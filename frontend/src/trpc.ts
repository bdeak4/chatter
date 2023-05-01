import { createTRPCReact, httpBatchLink } from "@trpc/react-query";
import type { AppRouter } from "../../backend/src/routes/_app";
import superjson from "superjson";
import { env } from "./env";

export const trpc = createTRPCReact<AppRouter>();

export const createTRPCClient = () => {
  return trpc.createClient({
    transformer: superjson,
    links: [httpBatchLink({ url: env.VITE_TRPC_ENDPOINT })],
  });
};
