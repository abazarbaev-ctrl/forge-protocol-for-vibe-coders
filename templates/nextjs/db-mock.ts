/**
 * Forge Protocol — Prisma Mock Template (Next.js + Vitest)
 * Source: Zeen AI Tutor (5/5 quality)
 *
 * Manual vi.fn() mocks give full control over each test.
 * Each test can override specific model methods via vi.mocked().
 *
 * Usage:
 *   // In your test file:
 *   vi.mock("@/lib/db", () => import("./__mocks__/db"));
 *   import { prisma } from "@/lib/db";
 *   const mockedPrisma = vi.mocked(prisma, true);
 *
 *   beforeEach(() => vi.clearAllMocks());
 *
 *   it("test case", async () => {
 *     mockedPrisma.user.findUnique.mockResolvedValue({ id: "1", name: "Test" } as never);
 *     // ... test logic
 *   });
 *
 * Save as: src/lib/__mocks__/db.ts
 * Adapt the model names and methods to match your prisma/schema.prisma
 */

import { vi } from "vitest";

export const prisma = {
  // --- ADAPT THESE MODELS TO YOUR SCHEMA ---
  user: {
    findUnique: vi.fn(),
    findMany: vi.fn(),
    create: vi.fn(),
    update: vi.fn(),
    delete: vi.fn(),
    count: vi.fn(),
  },
  // Add more models as needed:
  // post: {
  //   findUnique: vi.fn(),
  //   findMany: vi.fn(),
  //   create: vi.fn(),
  //   update: vi.fn(),
  //   delete: vi.fn(),
  // },
};
