import { prisma } from "../src/prisma";
import { log } from "../src/logger";

async function main() {
  await prisma.user.create({
    data: {
      name: "Admin",
    },
  });
  log.info("seeded");
}

main()
  .then(async () => {
    await prisma.$disconnect();
  })
  .catch(async (e) => {
    log.error(e);
    await prisma.$disconnect();
    process.exit(1);
  });
