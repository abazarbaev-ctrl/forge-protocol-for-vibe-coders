/**
 * Forge Protocol — Error Boundary Template (Next.js 14)
 * Source: Zeen AI Tutor (5/5 quality)
 *
 * Catches React rendering errors. Logs structured JSON for Vercel.
 * Mount in layout.tsx wrapping {children}.
 *
 * Usage:
 *   import { ErrorBoundary } from "@/components/ErrorBoundary";
 *   <ErrorBoundary>{children}</ErrorBoundary>
 */

"use client";

import React from "react";

interface Props {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error(
      JSON.stringify({
        event: "error_boundary",
        message: error.message,
        stack: (error.stack || "").slice(0, 1000),
        componentStack: (info.componentStack || "").slice(0, 500),
        url: typeof window !== "undefined" ? window.location.href : "",
        timestamp: new Date().toISOString(),
      })
    );
  }

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) return this.props.fallback;
      return (
        <div className="p-6 m-4 bg-red-50 border border-red-200 rounded-xl text-center">
          <div className="text-lg font-bold text-red-600 mb-2">
            Something went wrong
          </div>
          <div className="text-sm text-gray-500 mb-4">
            {this.state.error?.message || "Unknown error"}
          </div>
          <button
            onClick={() => this.setState({ hasError: false, error: null })}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg text-sm font-medium hover:bg-blue-600"
          >
            Try again
          </button>
          <button
            onClick={() => window.location.reload()}
            className="ml-2 px-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-600 hover:bg-gray-50"
          >
            Reload page
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}
