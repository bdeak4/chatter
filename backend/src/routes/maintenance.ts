import { publicProcedure, router } from "../trpc";

export const maintenance = router({
  healthz: publicProcedure.query(async ({ ctx }) => {
    await ctx.prisma.$queryRaw`SELECT 1`;
    return "ok";
  }),
});
