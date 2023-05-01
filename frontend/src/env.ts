import { z } from "zod";

const schema = z.object({
  NODE_ENV: z.enum(["development", "production"]).default("development"),
  VITE_TRPC_ENDPOINT: z.string().url().default("http://localhost:4000/trpc"),
});

const parsed = schema.safeParse(import.meta.env);

if (!parsed.success) {
  if (import.meta.env.DEV) {
    alert("invalid environment variables, check console");
  }
  const err = JSON.stringify(parsed.error.format(), null, 2);
  throw `invalid environment variables ${err}`;
}

export const env = parsed.data;

if (import.meta.env.DEV) {
  console.log("environment variables", env);
}
