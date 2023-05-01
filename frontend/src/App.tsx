import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { httpBatchLink } from "@trpc/client";
import { useState } from "react";
import { trpc } from "./trpc";
import superjson from "superjson";
import Page from "./page";
import { env } from "./env";

function App() {
  const [queryClient] = useState(() => new QueryClient());
  const [trpcClient] = useState(() =>
    trpc.createClient({
      transformer: superjson,
      links: [httpBatchLink({ url: env.VITE_TRPC_ENDPOINT })],
    })
  );

  return (
    <trpc.Provider client={trpcClient} queryClient={queryClient}>
      <QueryClientProvider client={queryClient}>
        <h1>Vite + React</h1>
        <Page />
      </QueryClientProvider>
    </trpc.Provider>
  );
}

export default App;
