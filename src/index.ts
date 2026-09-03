/**
 * PipeFish Labs - Edge Routing Proxy & Security Gateway
 * High-performance edge worker for routing, security header injection, and health checks.
 */

export interface Env {
  UPSTREAM_URL?: string;
  ENVIRONMENT?: string;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    const upstream = env.UPSTREAM_URL || "https://pipefishlabs.io";

    // 1. Edge Health & Status Check Endpoint
    if (url.pathname === "/health" || url.pathname === "/api/health") {
      return new Response(
        JSON.stringify({
          status: "healthy",
          service: "pipefish-labs-edge-proxy",
          timestamp: new Date().toISOString(),
          region: request.cf?.colo || "global",
          protocol: request.cf?.httpProtocol || "HTTP/3",
          security: "Zero-Trust TLS 1.3 / Post-Quantum Ready",
        }),
        {
          status: 200,
          headers: {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "X-Edge-Router": "PipeFish-Cloudflare-Worker",
          },
        }
      );
    }

    // 2. Handle CORS Preflight for API / MCP Endpoints
    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type, Authorization, X-API-Key, X-Agent-ID",
          "Access-Control-Max-Age": "86400",
        },
      });
    }

    // 3. Forward request to Upstream
    const upstreamUrl = new URL(url.pathname + url.search, upstream);
    const modifiedRequest = new Request(upstreamUrl.toString(), {
      method: request.method,
      headers: request.headers,
      body: request.body,
      redirect: "follow",
    });

    try {
      const response = await fetch(modifiedRequest);
      const newHeaders = new Headers(response.headers);

      // 4. Inject Enterprise Zero-Trust Security Headers
      newHeaders.set("X-Edge-Proxy", "PipeFish-Labs-Cloudflare");
      newHeaders.set("X-Content-Type-Options", "nosniff");
      newHeaders.set("X-Frame-Options", "DENY");
      newHeaders.set("Referrer-Policy", "strict-origin-when-cross-origin");
      newHeaders.set(
        "Strict-Transport-Security",
        "max-age=63072000; includeSubDomains; preload"
      );

      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers: newHeaders,
      });
    } catch (error) {
      return new Response(
        JSON.stringify({
          error: "Edge routing upstream error",
          message: error instanceof Error ? error.message : "Unknown error",
        }),
        {
          status: 502,
          headers: { "Content-Type": "application/json" },
        }
      );
    }
  },
};
