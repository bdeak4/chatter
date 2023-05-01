import { trpc } from "../trpc";

export const HomePage = () => {
  const healthzQuery = trpc.maintenance.healthz.useQuery();

  if (healthzQuery.isLoading) {
    return <div>Loading...</div>;
  }

  if (healthzQuery.isError) {
    return (
      <div>
        Error: <pre>{JSON.stringify(healthzQuery.error.message, null, 2)}</pre>
      </div>
    );
  }

  return (
    <div>
      <pre>{JSON.stringify(healthzQuery.data, null, 2)}</pre>
    </div>
  );
};
