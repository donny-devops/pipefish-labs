/**
 * PipeFish Labs - Edge Routing Proxy & Security Gateway
 * High-performance edge worker serving site via Cloudflare Workers Static Assets
 * with zero-trust security header injection, CORS preflight, and health telemetry.
 */

export interface Env {
  ENVIRONMENT?: string;
  UPSTREAM_URL?: string;
  ASSETS?: {
    fetch: (request: Request | string) => Promise<Response>;
  };
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);

    // 1. Edge Health & Status Check Endpoint
    if (url.pathname === "/health" || url.pathname === "/api/health") {
      return new Response(
        JSON.stringify({
          status: "healthy",
          service: "pipefish-labs-edge-proxy",
          timestamp: new Date().toISOString(),
          region: (request as any).cf?.colo || "global",
          protocol: (request as any).cf?.httpProtocol || "HTTP/3",
          delivery: env.ASSETS ? "Workers Static Assets" : "Origin Proxy",
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

    // Helper to inject zero-trust enterprise security headers
    const applySecurityHeaders = (headers: Headers): Headers => {
      const newHeaders = new Headers(headers);
      newHeaders.set("X-Edge-Proxy", "PipeFish-Labs-Cloudflare");
      newHeaders.set("X-Content-Type-Options", "nosniff");
      newHeaders.set("X-Frame-Options", "DENY");
      newHeaders.set("Referrer-Policy", "strict-origin-when-cross-origin");
      newHeaders.set(
        "Strict-Transport-Security",
        "max-age=63072000; includeSubDomains; preload"
      );
      return newHeaders;
    };

    // 3. Serve from Cloudflare Workers Static Assets binding directly
    if (env.ASSETS) {
      try {
        const assetResponse = await env.ASSETS.fetch(request);
        // If asset is found or we have no alternative upstream, serve the asset response (including 404.html)
        if (assetResponse.status !== 404 || !env.UPSTREAM_URL) {
          const securedHeaders = applySecurityHeaders(assetResponse.headers);
          return new Response(assetResponse.body, {
            status: assetResponse.status,
            statusText: assetResponse.statusText,
            headers: securedHeaders,
          });
        }
      } catch (assetErr) {
        console.warn("[ASSETS] Static asset fetch error, falling back to upstream if configured:", assetErr);
      }
    }

    // 4. Fallback to Upstream URL (if ASSETS binding not present or upstream fallback needed)
    const upstream = env.UPSTREAM_URL || "https://pipefishlabs.io";
    const upstreamUrl = new URL(url.pathname + url.search, upstream);
    const modifiedRequest = new Request(upstreamUrl.toString(), {
      method: request.method,
      headers: request.headers,
      body: request.body,
      redirect: "follow",
    });

    try {
      const response = await fetch(modifiedRequest);
      const securedHeaders = applySecurityHeaders(response.headers);
      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers: securedHeaders,
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
