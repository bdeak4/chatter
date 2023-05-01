import express from "express";
import pino from "pino-http";
import * as trpcExpress from "@trpc/server/adapters/express";
import { createContext } from "./context";
import { appRouter } from "./router";
import { env } from "./env";
import { log } from "./logger";

const app = express();

app.use(pino());

app.use(
  "/api/trpc",
  trpcExpress.createExpressMiddleware({
    router: appRouter,
    createContext,
  })
);

app.listen(env.PORT, () => {
  log.info(`app listening on port ${env.PORT}`);
});
