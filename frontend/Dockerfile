FROM node:20-alpine AS base

WORKDIR /app

# Instalar dependências primeiro (cache layer)
COPY package*.json ./
RUN npm ci

# Copiar código
COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
