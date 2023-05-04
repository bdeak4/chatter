import pino from "pino";
import { env } from "./env";

const transport =
  env.NODE_ENV === "development"
    ? pino.transport({ target: "pino-pretty" })
    : undefined;

export const log = pino(transport);
