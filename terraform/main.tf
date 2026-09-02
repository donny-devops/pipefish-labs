terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.40"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.26"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.12"
    }
  }
}

provider "aws" {
  region = var.region
  default_tags {
    tags = {
      Project     = "PipeFish-Labs"
      Environment = var.environment
      ManagedBy   = "Terraform"
      Security    = "Zero-Trust-ZDR"
    }
  }
}

# 1. VPC with Private Subnets for Isolated Enclaves
resource "aws_vpc" "mesh_vpc" {
  cidr_block           = "10.100.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "${var.cluster_name}-vpc"
  }
}

# 2. Security Group Enforcing Least-Privilege Inter-Agent Traffic
resource "aws_security_group" "mesh_sg" {
  name        = "${var.cluster_name}-sg"
  description = "Controls inter-agent mesh traffic with strict port scoping"
  vpc_id      = aws_vpc.mesh_vpc.id

  ingress {
    description = "mTLS Inter-Node gRPC & MCP Traffic"
    from_port   = 8000
    to_port     = 8443
    protocol    = "tcp"
    self        = true
  }

  egress {
    description = "Allow Outbound HTTPS for External Model APIs"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.cluster_name}-security-group"
  }
}

# 3. KMS Key with Automated Rotation for Enclave Payload Encryption
resource "aws_kms_key" "enclave_pqc_kms_key" {
  description             = "PipeFish Labs Master Cryptographic Key for Multi-Agent Payload Signing"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  tags = {
    Name = "${var.cluster_name}-kms-key"
  }
}
