import * as dotenv from "dotenv";
import { z } from "zod";

dotenv.config();

const schema = z.object({
  PORT: z.coerce.number().int().default(4001),
  NODE_ENV: z.enum(["development", "production"]).default("development"),
  // prisma
  DATABASE_URL: z.string().url(),
  LOG_QUERY_THRESHOLD_MS: z.coerce.number().int().default(0),
});

const parsed = schema.safeParse(process.env);

if (!parsed.success) {
  console.error("invalid environment variables", parsed.error.format());
  process.exit(1);
}

export const env = parsed.data;
