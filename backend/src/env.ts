import * as dotenv from "dotenv";
import { z } from "zod";

dotenv.config();

const envSchema = z.object({
  // express
  PORT: z.number().default(4000),
  NODE_ENV: z.enum(["development", "production"]),
  // prisma
  DATABASE_URL: z.string().url(),
});

const parsedSchema = envSchema.safeParse(process.env);

if (!parsedSchema.success) {
  console.error(
    "Invalid environment variables:",
    JSON.stringify(parsedSchema.error.format(), null, 4)
  );
  process.exit(1);
}

export const env = parsedSchema.data;

console.log("env:", env);
