/**
 * Forge Protocol — Auth Middleware Template (Next.js 14)
 * Source: Zeen AI Tutor (5/5 quality)
 *
 * Cookie-based role validation with regex route matching.
 * Integrates page-view telemetry inline.
 *
 * Adapt:
 * - PROTECTED_ROUTES regex patterns for your app's routes
 * - Cookie name and structure
 * - Login redirect paths
 *
 * Copy to: src/middleware.ts (Next.js root)
 */

import { NextRequest, NextResponse } from "next/server";

// --- ADAPT THESE TO YOUR APP ---
const USER_ROUTES = /^\/dashboard\/([^/]+)/;  // e.g., /dashboard/:userId
const ADMIN_ROUTES = /^\/admin/;
const API_ROUTES = /^\/api\/(protected|data)/;  // API routes requiring auth
const AUTH_COOKIE = "app_auth";  // Cookie name
const LOGIN_PATH = "/";  // Redirect target for unauthenticated users

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Telemetry: log every page view as structured JSON (Vercel picks this up)
  console.log(
    JSON.stringify({
      event: "page_view",
      path: pathname,
      timestamp: new Date().toISOString(),
      ua: request.headers.get("user-agent")?.slice(0, 100) || "",
    })
  );

  // Auth: check user routes
  const userMatch = pathname.match(USER_ROUTES);
  if (userMatch) {
    const authCookie = request.cookies.get(AUTH_COOKIE)?.value;
    if (!authCookie) {
      const url = request.nextUrl.clone();
      url.pathname = LOGIN_PATH;
      url.searchParams.set("login", userMatch[1]);
      return NextResponse.redirect(url);
    }

    try {
      const auth = JSON.parse(authCookie);
      // Verify the user ID matches the route (prevent cross-user access)
      if (auth.userId !== userMatch[1]) {
        const url = request.nextUrl.clone();
        url.pathname = LOGIN_PATH;
        return NextResponse.redirect(url);
      }
    } catch {
      const url = request.nextUrl.clone();
      url.pathname = LOGIN_PATH;
      return NextResponse.redirect(url);
    }
  }

  // Auth: check admin routes
  if (ADMIN_ROUTES.test(pathname)) {
    const authCookie = request.cookies.get(AUTH_COOKIE)?.value;
    if (!authCookie) {
      const url = request.nextUrl.clone();
      url.pathname = LOGIN_PATH;
      url.searchParams.set("login", "admin");
      return NextResponse.redirect(url);
    }

    try {
      const auth = JSON.parse(authCookie);
      if (auth.role !== "admin") {
        const url = request.nextUrl.clone();
        url.pathname = LOGIN_PATH;
        return NextResponse.redirect(url);
      }
    } catch {
      const url = request.nextUrl.clone();
      url.pathname = LOGIN_PATH;
      return NextResponse.redirect(url);
    }
  }

  // Auth: check protected API routes — require valid cookie on POST
  if (API_ROUTES.test(pathname) && request.method === "POST") {
    const authCookie = request.cookies.get(AUTH_COOKIE)?.value;
    if (!authCookie) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/admin/:path*", "/api/:path*"],
};
