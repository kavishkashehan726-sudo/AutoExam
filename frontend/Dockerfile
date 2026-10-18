# Development image. Production runs `next start` under PM2 (see docs/DEPLOY.md).
FROM node:24-slim

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev", "--", "--hostname", "0.0.0.0"]
