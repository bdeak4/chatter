import express from "express";
import pino from "pino-http";
import cors from "cors";
import { createExpressMiddleware } from "@trpc/server/adapters/express";
import { createContext } from "./trpc";
import { env } from "./env";
import { log } from "./logger";
import { appRouter } from "./routes";

const app = express();

app.use(pino());
app.use(cors({ origin: env.FRONTEND_ENDPOINT, credentials: true }));

app.use(
  "/trpc",
  createExpressMiddleware({
    router: appRouter,
    createContext,
  })
);

app.listen(env.PORT, () => {
  log.info(`app listening on port ${env.PORT}`);
});
