# PipeFish Labs — Terraform Cloudflare Zero-Trust Tunnel Configuration

terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.25"
    }
  }
}

resource "cloudflare_tunnel" "agent_mesh_tunnel" {
  account_id = "placeholder_cloudflare_account_id"
  name       = "pipefish-mesh-tunnel"
  secret     = "placeholder_tunnel_secret_base64"
}

resource "cloudflare_tunnel_config" "mesh_tunnel_config" {
  account_id = "placeholder_cloudflare_account_id"
  tunnel_id  = cloudflare_tunnel.agent_mesh_tunnel.id

  config {
    ingress_rule {
      hostname = "api.pipefishlabs.io"
      service  = "http://localhost:8000"
    }
    ingress_rule {
      hostname = "ws.pipefishlabs.internal"
      service  = "http://localhost:8001"
    }
    ingress_rule {
      service = "http_status:404"
    }
  }
}

resource "cloudflare_record" "api_tunnel_cname" {
  zone_id = var.cloudflare_zone_id
  name    = "api"
  value   = "${cloudflare_tunnel.agent_mesh_tunnel.id}.cfargotunnel.com"
  type    = "CNAME"
  proxied = true
}
