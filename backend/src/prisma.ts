import { PrismaClient } from "@prisma/client";
import { log } from "./logger";
import { env } from "./env";

export const prisma = new PrismaClient({ log: ["warn", "error"] });

prisma.$use(async (params, next) => {
  const before = Date.now();

  const result = await next(params);

  const responseTime = Date.now() - before;

  if (responseTime > env.LOG_QUERY_THRESHOLD_MS) {
    if (env.LOG_QUERY_THRESHOLD_MS > 0) {
      log.warn({ ...params, responseTime }, "slow prisma query");
    } else {
      log.info({ ...params, responseTime }, "prisma query");
    }
  }

  return result;
});
