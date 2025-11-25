import os, itertools, time
from collections import deque, defaultdict
from datetime import datetime, timedelta
from typing import List

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response
import httpx

# ---------- Config ----------
# UPSTREAMS: lista de serviços backend (APIs Node e Python)
# Pode ser configurado via variável de ambiente para escalar dinamicamente
UPSTREAMS = [u.strip().rstrip("/") for u in os.getenv("UPSTREAMS","http://api-node-1:3000,http://api-node-2:3000,http://api-python-1:8000,http://api-python-2:8000").split(",") if u.strip()]

# Rate Limit: limite de requisições por IP
RATE_LIMIT = int(os.getenv("RATE_LIMIT","1000"))  # 100 req/min por padrão
WINDOW_SEC = int(os.getenv("WINDOW_SEC","60"))

# Circuit Breaker: proteção contra serviços com falha
CB_FAIL_THRESHOLD = int(os.getenv("CB_FAIL_THRESHOLD","5"))  # 5 falhas antes de abrir
CB_COOLDOWN_SEC = int(os.getenv("CB_COOLDOWN_SEC","30"))  # 30s de cooldown

# ---------- App ----------
app = FastAPI(
    title="API Gateway - User Benchmark",
    description="Gateway com Round Robin, Circuit Breaker e Rate Limiting",
    version="1.0.0",
    docs_url="/_docs"
)

# Rate limit (per IP)
_recent = defaultdict(deque)  # ip -> timestamps
_window = timedelta(seconds=WINDOW_SEC)

# Round-robin: distribuição circular entre upstreams
_rr = itertools.cycle(range(len(UPSTREAMS)))

# Circuit breaker per upstream
# state: "closed" (normal) | "open" (bloqueado) | "half" (teste)
_cb = {
    i: {"state":"closed","fail":0,"opened_at":0.0}
    for i in range(len(UPSTREAMS))
}

# Métricas para monitoramento
_metrics = {
    i: {"total":0, "success":0, "failure":0}
    for i in range(len(UPSTREAMS))
}

def _client_ip(req: Request) -> str:
    """Extrai o IP do cliente (considera proxy)"""
    fwd = req.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    return req.client.host or "?"

def _rate_limit(ip: str) -> bool:
    """
    Rate limiting por IP usando sliding window.
    Retorna True se o limite foi excedido.
    """
    now = datetime.utcnow()
    q = _recent[ip]
    # Remove timestamps fora da janela
    while q and (now - q[0]) > _window:
        q.popleft()
    if len(q) >= RATE_LIMIT:
        return True
    q.append(now)
    return False

def _pick_upstream_index() -> int:
    """
    Seleciona o próximo upstream usando Round Robin.
    Pula upstreams com circuit breaker OPEN (a menos que o cooldown tenha passado).
    """
    for _ in range(len(UPSTREAMS)):
        i = next(_rr)
        st = _cb[i]
        if st["state"] == "open":
            # Verifica se pode tentar novamente (half-open)
            if (time.time() - st["opened_at"]) >= CB_COOLDOWN_SEC:
                st["state"] = "half"
                return i
            # Ainda em cooldown, pula para o próximo
            continue
        return i
    # Se todos os upstreams estão OPEN
    raise HTTPException(status_code=503, detail="No healthy upstreams (all circuits open)")

def _on_success(i: int):
    """Registra sucesso: reseta falhas e fecha o circuit breaker"""
    st = _cb[i]
    st["fail"] = 0
    st["state"] = "closed"
    _metrics[i]["success"] += 1

def _on_failure(i: int):
    """Registra falha: incrementa contador e pode abrir o circuit breaker"""
    st = _cb[i]
    st["fail"] += 1
    _metrics[i]["failure"] += 1
    # Se estava em half-open ou atingiu o threshold, abre o circuito
    if st["state"] == "half" or st["fail"] >= CB_FAIL_THRESHOLD:
        st["state"] = "open"
        st["opened_at"] = time.time()

# Headers que não devem ser repassados (hop-by-hop)
HOP = {"connection","keep-alive","proxy-authenticate","proxy-authorization","te","trailers","transfer-encoding","upgrade"}

@app.middleware("http")
async def rate_limit_middleware(req: Request, call_next):
    """Middleware de rate limiting aplicado a todas as requisições"""
    if _rate_limit(_client_ip(req)):
        raise HTTPException(
            status_code=429, 
            detail=f"Rate limit exceeded ({RATE_LIMIT} requests per {WINDOW_SEC}s)"
        )
    return await call_next(req)

@app.api_route("/{path:path}", methods=["GET","POST","PUT","PATCH","DELETE","HEAD","OPTIONS"])
async def proxy(req: Request, path: str):
    """
    Endpoint principal do gateway: faz proxy de todas as requisições para os upstreams.
    Utiliza Round Robin para distribuir a carga.
    """
    i = _pick_upstream_index()
    upstream = UPSTREAMS[i]
    _metrics[i]["total"] += 1
    
    # Constrói a URL completa
    url = f"{upstream}/" + (path or "")
    if req.url.query:
        url += f"?{req.url.query}"
    
    body = await req.body()
    headers = {k:v for k,v in req.headers.items() if k.lower() not in HOP}

    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=False) as c:
            r = await c.request(req.method, url, headers=headers, content=body)
    except Exception as e:
        _on_failure(i)
        raise HTTPException(status_code=502, detail=f"Bad gateway (upstream error: {str(e)})")

    # Trata 500+ como falha para o circuit breaker
    if r.status_code >= 500:
        _on_failure(i)
    else:
        _on_success(i)

    resp_headers = {k:v for k,v in r.headers.items() if k.lower() not in HOP}
    return Response(
        content=r.content, 
        status_code=r.status_code, 
        headers=resp_headers, 
        media_type=r.headers.get("content-type")
    )

@app.get("/_health")
def health():
    """Endpoint de health check com informações do gateway"""
    return {
        "status": "healthy",
        "upstreams": UPSTREAMS,
        "circuit_breakers": _cb,
        "metrics": _metrics,
        "config": {
            "rate_limit": RATE_LIMIT,
            "window_sec": WINDOW_SEC,
            "cb_fail_threshold": CB_FAIL_THRESHOLD,
            "cb_cooldown_sec": CB_COOLDOWN_SEC
        }
    }

@app.get("/_metrics")
def metrics():
    """Endpoint detalhado de métricas para análise de desempenho"""
    return {
        "upstreams": [
            {
                "url": UPSTREAMS[i],
                "state": _cb[i]["state"],
                "failures": _cb[i]["fail"],
                "total_requests": _metrics[i]["total"],
                "successful_requests": _metrics[i]["success"],
                "failed_requests": _metrics[i]["failure"],
                "success_rate": round(_metrics[i]["success"] / _metrics[i]["total"] * 100, 2) if _metrics[i]["total"] > 0 else 0
            }
            for i in range(len(UPSTREAMS))
        ],
        "total_requests": sum(_metrics[i]["total"] for i in range(len(UPSTREAMS)))
    }
