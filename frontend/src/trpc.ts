import { createTRPCReact, httpBatchLink } from "@trpc/react-query";
import type { AppRouter } from "../../backend/src/routes/_app";
import superjson from "superjson";
import { env } from "./env";
import { QueryClient } from "@tanstack/react-query";

export const trpc = createTRPCReact<AppRouter>();

export const createTRPCClient = () => {
  return trpc.createClient({
    transformer: superjson,
    links: [httpBatchLink({ url: env.VITE_TRPC_ENDPOINT })],
  });
};

export const createQueryClient = () => {
  return new QueryClient({
    defaultOptions: {
      queries: {
        cacheTime: 1000 * 60 * 10,
        staleTime: 30 * 1000,
        retryDelay: 2000,
      },
    },
  });
};
