FROM node:18-slim
WORKDIR /app
ENV NODE_ENV production
ENV PORT 4001
EXPOSE 4001
HEALTHCHECK CMD curl -f http://localhost:4001/trpc/maintenance.healthz || exit 1
LABEL org.opencontainers.image.source https://github.com/bdeak4/chatter

RUN apt-get update && apt-get install -y curl cron && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY package.json yarn.lock ./
COPY prisma ./prisma/

RUN yarn install --immutable && yarn cache clean

COPY . .

CMD [ "sh", "-c", "yarn prod:db-migrate; yarn prod:server" ]
