import * as dotenv from "dotenv";
import { z } from "zod";
import { log } from "./logger";

dotenv.config();

const schema = z.object({
  // express
  PORT: z.number().default(4000),
  NODE_ENV: z.enum(["development", "production"]),
  // prisma
  DATABASE_URL: z.string().url(),
});

const parsed = schema.safeParse(process.env);

if (!parsed.success) {
  log.error(parsed.error.format(), "invalid environment variables");
  process.exit(1);
}

export const env = parsed.data;

log.info(env, "environment variables");
