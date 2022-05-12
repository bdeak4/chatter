# chatter

...which cryptocurrencies are people talking about today?

![](https://bdeak.net/img/chatter.png)

## Setup

Development:

```bash
$ git clone https://github.com/bdeak4/chatter
$ cd chatter
$ cp .env.example .env
$ docker-compose up --build
```

Production:

```bash
$ docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
```
