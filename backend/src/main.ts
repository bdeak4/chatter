import express from "express";
import * as trpcExpress from "@trpc/server/adapters/express";
import { router } from "./trpc";
import { createContext } from "./context";
import { maintenanceRouter } from "./routes/maintenance";

const appRouter = router({
  maintenance: maintenanceRouter,
});

export type AppRouter = typeof appRouter;

const app = express();

app.use(
  "/trpc",
  trpcExpress.createExpressMiddleware({
    router: appRouter,
    createContext,
  })
);

const port = process.env.PORT || 4000;
app.listen(port, () => {
  console.log(`[express] app listening on port ${port}`);
});
