import { publicProcedure, router } from "../trpc";
import { z } from "zod";

export const maintenanceRouter = router({
  healthz: publicProcedure.query(async ({ ctx }) => {
    await ctx.prisma.$queryRaw`SELECT 1`;
    return "ok";
  }),
  echo: publicProcedure.input(z.string()).query(async (input) => {
    return input;
  }),
});
