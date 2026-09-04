/**
 * PipeFish Labs - Edge Worker
 *
 * The website itself is served by Cloudflare's static asset layer, which runs
 * before this script. This Worker only handles the few paths that are not
 * static files, and falls back to the asset layer for everything else.
 */

export interface Env {
  ASSETS: Fetcher;
  ENVIRONMENT?: string;
}

const CORS_HEADERS: Record<string, string> = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, X-API-Key, X-Agent-ID",
  "Access-Control-Max-Age": "86400",
};

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    // 1. Edge health and status endpoint.
    if (url.pathname === "/health" || url.pathname === "/api/health") {
      return new Response(
        JSON.stringify({
          status: "healthy",
          service: "pipefish-labs-edge",
          environment: env.ENVIRONMENT ?? "unknown",
          timestamp: new Date().toISOString(),
          region: (request.cf?.colo as string | undefined) ?? "global",
        }),
        {
          status: 200,
          headers: {
            "Content-Type": "application/json",
            "Cache-Control": "no-store",
          },
        }
      );
    }

    // 2. CORS preflight for the published API specs under /sdk/.
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }

    // 3. Everything else is a static asset. Unmatched paths resolve to 404.html
    //    with a 404 status, per not_found_handling in wrangler.jsonc.
    return env.ASSETS.fetch(request);
  },
};
