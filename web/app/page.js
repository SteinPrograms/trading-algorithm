import Image from 'next/image'



export default function Home() {
  const { PrismaClient } = require('@prisma/client')

  const prisma = new PrismaClient()
  const positions = []
  async function main() {
    (await prisma.positions.findMany()).map(position => {
      positions.push(position)
    });
    console.log(positions)
  }

  main()
    .then(async () => {
      await prisma.$disconnect()
    })
    .catch(async (e) => {
      console.error(e)
      await prisma.$disconnect()
      process.exit(1)
    })




  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="flex flex-col items-center justify-center">
        <h1 className="text-6xl font-bold text-center">Welcome to the <span className="text-blue-500">Job</span> Board</h1>
        <p className="text-2xl text-center">
          Find your dream job today
          {positions}
        </p>
      </div>
    </main>
  )
}
