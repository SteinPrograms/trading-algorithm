/*
  Warnings:

  - You are about to drop the `Post` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `Profile` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `User` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropForeignKey
ALTER TABLE "Post" DROP CONSTRAINT "Post_authorId_fkey";

-- DropForeignKey
ALTER TABLE "Profile" DROP CONSTRAINT "Profile_userId_fkey";

-- DropTable
DROP TABLE "Post";

-- DropTable
DROP TABLE "Profile";

-- DropTable
DROP TABLE "User";

-- CreateTable
CREATE TABLE "positions" (
    "position_id" SERIAL NOT NULL,
    "time" VARCHAR(255) NOT NULL,
    "symbol" VARCHAR(255) NOT NULL,
    "yield" VARCHAR(255) NOT NULL,
    "wallet_value" VARCHAR(255) NOT NULL,

    CONSTRAINT "positions_pkey" PRIMARY KEY ("position_id")
);

-- CreateTable
CREATE TABLE "server" (
    "id" INTEGER NOT NULL,
    "current_status" VARCHAR(255) NOT NULL,
    "total_yield" VARCHAR(255) NOT NULL,
    "running_time" VARCHAR(255) NOT NULL,

    CONSTRAINT "server_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "target" (
    "id" INTEGER NOT NULL,
    "symbol" VARCHAR(255) NOT NULL,
    "buy_price" VARCHAR(255) NOT NULL,
    "sell_price" VARCHAR(255) NOT NULL,

    CONSTRAINT "target_pkey" PRIMARY KEY ("id")
);
