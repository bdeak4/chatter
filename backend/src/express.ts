import express from "express";
import pino from "pino-http";
import cors from "cors";
import compression from "compression";
import { createExpressMiddleware } from "@trpc/server/adapters/express";
import { createContext } from "./trpc";
import { env } from "./env";
import { log } from "./logger";
import { appRouter } from "./routes/_app";

const app = express();

app.use(pino());
app.use(cors());
app.use(compression());

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
