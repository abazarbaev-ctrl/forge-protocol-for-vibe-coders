/**
 * Forge Protocol — Global Error Handler Template (Next.js 14)
 * Source: Zeen AI Tutor (5/5 quality)
 *
 * Catches JS errors OUTSIDE React's ErrorBoundary:
 * - window.onerror (uncaught exceptions)
 * - unhandledrejection (unhandled async errors)
 *
 * Mount once in layout.tsx:
 *   import { GlobalErrorHandler } from "@/components/GlobalErrorHandler";
 *   <GlobalErrorHandler />
 */

"use client";

import { useEffect } from "react";

export function GlobalErrorHandler() {
  useEffect(() => {
    function handleError(event: ErrorEvent) {
      // Skip cross-origin script errors (browser security restriction)
      if (event.filename && !event.filename.includes(window.location.origin))
        return;
      console.error(
        JSON.stringify({
          event: "uncaught_error",
          message: event.message || "Unknown error",
          stack:
            event.error?.stack ||
            `${event.filename}:${event.lineno}:${event.colno}`,
          url: window.location.href,
          timestamp: new Date().toISOString(),
        })
      );
    }

    function handleRejection(event: PromiseRejectionEvent) {
      const reason = event.reason;
      console.error(
        JSON.stringify({
          event: "unhandled_rejection",
          message: reason?.message || String(reason || "Unhandled rejection"),
          stack: reason?.stack || "",
          url: window.location.href,
          timestamp: new Date().toISOString(),
        })
      );
    }

    window.addEventListener("error", handleError);
    window.addEventListener("unhandledrejection", handleRejection);
    return () => {
      window.removeEventListener("error", handleError);
      window.removeEventListener("unhandledrejection", handleRejection);
    };
  }, []);

  return null;
}
