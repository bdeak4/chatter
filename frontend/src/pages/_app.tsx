import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useState } from "react";
import { createTRPCClient, trpc } from "../trpc";
import { HomePage } from "./home";

function App() {
  const [queryClient] = useState(() => new QueryClient());
  const [trpcClient] = useState(() => createTRPCClient());

  return (
    <trpc.Provider client={trpcClient} queryClient={queryClient}>
      <QueryClientProvider client={queryClient}>
        <h1>Vite + React</h1>
        <HomePage />
      </QueryClientProvider>
    </trpc.Provider>
  );
}

export default App;
