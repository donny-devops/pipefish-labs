variable "environment" {
  type        = string
  default     = "production"
  description = "Target deployment environment (production, staging, dev)"
}

variable "region" {
  type        = string
  default     = "us-east-1"
  description = "Cloud provider primary region for agent mesh cluster"
}

variable "enclave_instance_type" {
  type        = string
  default     = "c6i.2xlarge"
  description = "Nitro Enclave-enabled compute instance type with memory encryption"
}

variable "cluster_name" {
  type        = string
  default     = "pipefish-agent-mesh"
  description = "Name identifier for the Kubernetes multi-agent mesh cluster"
}

variable "cloudflare_zone_id" {
  type        = string
  default     = "placeholder_zone_id"
  description = "Cloudflare Zone ID for pipefishlabs.io WAF rules"
}
