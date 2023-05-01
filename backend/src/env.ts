import * as dotenv from "dotenv";
import { z } from "zod";
import { log } from "./logger";

dotenv.config();

const schema = z.object({
  PORT: z.coerce.number().default(4000),
  NODE_ENV: z.enum(["development", "production"]).default("development"),
  // prisma
  DATABASE_URL: z.string().url(),
  LOG_QUERY_THRESHOLD_MS: z.coerce.number().default(0),
  // app
  CORS_ORIGINS: z.array(z.string().url()).default(["http://localhost:4001"]),
});

const parsed = schema.safeParse({
  ...process.env,
  CORS_ORIGINS: process.env.CORS_ORIGINS?.split(","),
});

if (!parsed.success) {
  log.error(parsed.error.format(), "invalid environment variables");
  process.exit(1);
}

export const env = parsed.data;

log.info(env, "environment variables");
