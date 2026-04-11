/**
 * Forge Protocol — Vitest Configuration Template (Next.js 14)
 * Source: Zeen AI Tutor (5/5 quality)
 *
 * Node environment for unit tests (no DOM needed).
 * Path alias matching tsconfig for @/ imports.
 *
 * Copy to: vitest.config.ts (project root)
 */

import { defineConfig } from "vitest/config";
import { resolve } from "path";

export default defineConfig({
  test: {
    environment: "node",
    include: ["src/**/*.test.ts"],
  },
  resolve: {
    alias: {
      "@": resolve(__dirname, "./src"),
    },
  },
});
