import { router } from "./trpc";
import { maintenanceRouter } from "./routes/maintenance";

export const appRouter = router({
  maintenance: maintenanceRouter,
});

export type AppRouter = typeof appRouter;
