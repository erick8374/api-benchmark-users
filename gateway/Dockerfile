FROM python:3.12-slim

WORKDIR /app

# Instala dependências
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código
COPY main.py ./

# Configurações padrão (podem ser sobrescritas no docker-compose)
ENV UPSTREAMS="http://api-node:3000,http://api-python:8000"
ENV RATE_LIMIT=100
ENV WINDOW_SEC=60
ENV CB_FAIL_THRESHOLD=5
ENV CB_COOLDOWN_SEC=30

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
