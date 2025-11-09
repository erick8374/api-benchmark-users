# Etapa 1: build do TypeScript
FROM node:22-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Etapa 2: runtime
FROM node:22-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/.env .env

RUN npm install --omit=dev

CMD ["node", "dist/server.js"]
