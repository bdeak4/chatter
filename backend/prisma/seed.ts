import { prisma } from "../src/prisma";

async function main() {
  await prisma.user.create({
    data: {
      name: "Admin",
    },
  });
}

main()
  .then(async () => {
    await prisma.$disconnect();
  })
  .catch(async (e) => {
    console.error(e);
    await prisma.$disconnect();
    process.exit(1);
  });
