# API Benchmark - Sistema de Gerenciamento de Usuários


## 📋 Descrição do Projeto


Este projeto implementa um sistema de benchmark comparativo entre duas APIs RESTful desenvolvidas em diferentes tecnologias, ambas gerenciando a mesma entidade de usuários com persistência em PostgreSQL. O sistema inclui um gateway com balanceamento de carga para distribuir requisições entre múltiplas instâncias das APIs.


### Objetivos


- Comparar o desempenho entre APIs desenvolvidas em **Node.js (TypeScript/Express)** e **Python (FastAPI)**
- Implementar escalabilidade horizontal através de múltiplas instâncias
- Utilizar gateway com algoritmo de balanceamento **Round Robin**
- Realizar testes de carga e estresse
- Analisar métricas de desempenho, latência e throughput


## 🗃️ Entidade Base: Users


Todos os serviços gerenciam a seguinte estrutura de dados:


| Campo      | Tipo    | Descrição                           |
|------------|---------|-------------------------------------|
| id         | Integer | Identificador único (auto increment)|
| name       | String  | Nome completo do usuário           |
| email      | String  | Endereço de e-mail                 |
| username   | String  | Nome de usuário (login)            |
| password   | String  | Senha do usuário                   |


## 🚀 Tecnologias Utilizadas


### APIs


#### API Node.js
- **Linguagem:** TypeScript
- **Framework:** Express.js
- **ORM:** TypeORM
- **Validação:** Class Validator
- **Documentação:** Swagger


#### API Python
- **Linguagem:** Python 3.12
- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Validação:** Pydantic
- **Documentação:** Swagger


### Gateway
- **Linguagem:** Python 3.12
- **Framework:** FastAPI
- **Cliente HTTP:** httpx (assíncrono)
- **Algoritmo:** Round Robin
- **Recursos:** Circuit Breaker, Rate Limiting


### Infraestrutura
- **Banco de Dados:** PostgreSQL 17
- **Containerização:** Docker & Docker Compose
- **Orquestração:** Docker Compose
- **Rede:** Bridge Network customizada


### Endpoints do Gateway


| Método | Endpoint       | Descrição                              |
|--------|----------------|----------------------------------------|
| *      | /{path}        | Proxy para as APIs (Round Robin)       |
| GET    | /_health       | Status do gateway e upstreams          |
| GET    | /_metrics      | Métricas detalhadas de desempenho      |
| GET    | /_docs         | Documentação Swagger do gateway        |


### Instalação


1. **Clone o repositório:**
```bash
git clone https://github.com/erick8374/api-benchmark-users.git
cd api-benchmark-users
```


2. **Construa as imagens Docker (primeira vez ou após alterações):**
```bash
sudo docker-compose build
```


Este passo é necessário para:
- Primeira execução do projeto
- Após mudanças no código fonte
- Após alterações nos Dockerfiles
- Após mudanças nas dependências (package.json, requirements.txt)


3. **Inicie todos os serviços:**
```bash
sudo docker-compose up -d
```


4. **Verifique o status:**
```bash
sudo docker-compose ps
```


Todos os serviços devem estar com status "Up" e o PostgreSQL deve estar "healthy".


5. **Teste o gateway:**
```bash
curl http://localhost:8080/_health
```


## 👥 Contribuidores

- Érick Landim, Pedro Kuntz