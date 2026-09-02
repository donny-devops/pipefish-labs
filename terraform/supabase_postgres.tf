# PipeFish Labs — Supabase & RDS PostgreSQL Database Infrastructure

variable "db_password" {
  type        = string
  sensitive   = true
  description = "Master password for PostgreSQL database instance"
  default     = "change_in_production_env"
}

resource "aws_db_subnet_group" "db_subnets" {
  name        = "${var.cluster_name}-db-subnets"
  subnet_ids  = [aws_vpc.mesh_vpc.id] # In production, uses multi-AZ private subnets
  description = "Isolated subnets for PipeFish state database"
}

resource "aws_security_group" "db_sg" {
  name        = "${var.cluster_name}-db-sg"
  description = "Allow inbound PostgreSQL traffic strictly from internal agent mesh"
  vpc_id      = aws_vpc.mesh_vpc.id

  ingress {
    description     = "PostgreSQL mTLS Access from Agent Nodes"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.mesh_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
