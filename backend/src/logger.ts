import pino from "pino";
import { env } from "./env";

const transport = pino.transport({
  target: env.NODE_ENV === "development" ? "pino-pretty" : "pino/file",
});

export const log = pino(transport);
