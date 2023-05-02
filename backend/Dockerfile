FROM node:18
LABEL org.opencontainers.image.source https://github.com/bdeak4/chatter
WORKDIR /app

COPY package.json yarn.lock ./
COPY prisma ./prisma/

RUN yarn install --immutable

COPY . .

CMD [ "yarn", "prod:server" ]
