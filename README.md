# chatter

...which cryptocurrencies are people talking about today?

## Setup

Development:

```bash
$ git clone https://github.com/bdeak4/chatter
$ cd chatter
$ mv .env.empty .env
$ docker-compose build
$ docker-compose up
```

Production:

```bash
$ docker-compose build
$ docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```
