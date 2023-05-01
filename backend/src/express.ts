import express from "express";
import pino from "pino-http";
import { createExpressMiddleware } from "@trpc/server/adapters/express";
import { router, createContext } from "./trpc";
import { env } from "./env";
import { log } from "./logger";
import { appRouter } from "./routes";

const app = express();

app.use(pino());

app.use(
  "/api/trpc",
  createExpressMiddleware({
    router: appRouter,
    createContext,
  })
);

app.listen(env.PORT, () => {
  log.info(`app listening on port ${env.PORT}`);
});
