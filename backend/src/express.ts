import express from "express";
import compression from "compression";
import pino from "pino-http";
import cors from "cors";
import { createExpressMiddleware } from "@trpc/server/adapters/express";
import { createContext } from "./trpc";
import { env } from "./env";
import { log } from "./logger";
import { appRouter } from "./routes/_app";

const app = express();

app.use(compression());
app.use(pino());
app.use(cors({ origin: env.CORS_ORIGINS }));

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
