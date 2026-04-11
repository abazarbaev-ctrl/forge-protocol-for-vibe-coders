/**
 * Forge Protocol — Telemetry Module Template (Next.js 14)
 * Source: Zeen AI Tutor (5/5 quality)
 *
 * Zero-dependency structured JSON logging.
 * Vercel automatically ingests stdout/stderr as logs.
 *
 * Usage:
 *   import { logEvent, logError } from "@/lib/telemetry";
 *   logEvent("order_placed", { userId, total, items: cart.length });
 *   logError("payment_failed", error, { orderId });
 */

export function logEvent(
  event: string,
  data: Record<string, unknown> = {}
): void {
  console.log(
    JSON.stringify({
      event,
      ...data,
      timestamp: new Date().toISOString(),
    })
  );
}

export function logError(
  message: string,
  error?: unknown,
  context: Record<string, unknown> = {}
): void {
  console.error(
    JSON.stringify({
      event: "error",
      message,
      stack:
        error instanceof Error
          ? (error.stack || "").slice(0, 1000)
          : String(error),
      ...context,
      timestamp: new Date().toISOString(),
    })
  );
}
