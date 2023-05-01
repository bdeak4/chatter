import { router } from "../trpc";
import { maintenance } from "./maintenance";

export const appRouter = router({
  maintenance,
});

export type AppRouter = typeof appRouter;
