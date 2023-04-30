import * as trpcExpress from "@trpc/server/adapters/express";
import { createContext } from "./context";
import { publicProcedure, router } from "./trpc";
import express from "express";
import { maintenanceRouter } from "./routers/maintenance";

const app = express();

const appRouter = router({
  maintenance: maintenanceRouter,
  healthz: publicProcedure.query(async () => {
    return "ok";
  }),
});

app.use(
  "/trpc",
  trpcExpress.createExpressMiddleware({
    router: appRouter,
    createContext,
  })
);

const port = 4000;
app.listen(port, () => {
  console.log(`[express] app listening on port ${port}`);
});
