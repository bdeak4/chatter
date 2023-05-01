import { PrismaClient } from "@prisma/client";
import { log } from "./logger";

export const prisma = new PrismaClient({ log: ["warn", "error"] });

prisma.$use(async (params, next) => {
  const before = Date.now();

  const result = await next(params);

  const after = Date.now();

  log.info({ ...params, responseTime: after - before }, "prisma query");

  return result;
});
