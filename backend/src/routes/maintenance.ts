import { publicProcedure, router } from "../trpc";
import { z } from "zod";
import { log } from "../logger";

export const maintenanceRouter = router({
  healthz: publicProcedure.query(async ({ ctx }) => {
    await ctx.prisma.$queryRaw`SELECT 1`;
    return "ok";
  }),
  echo: publicProcedure
    .input(z.object({ text: z.string() }))
    .query(async ({ input }) => {
      log.info({ text: input.text }, "echo");
      return input.text;
    }),
});
