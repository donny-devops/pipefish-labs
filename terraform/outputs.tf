output "vpc_id" {
  value       = aws_vpc.mesh_vpc.id
  description = "Identifier of the isolated mesh VPC"
}

output "security_group_id" {
  value       = aws_security_group.mesh_sg.id
  description = "Identifier of the inter-agent security group"
}

output "kms_key_arn" {
  value       = aws_kms_key.enclave_pqc_kms_key.arn
  description = "ARN of the automated key rotation KMS key"
}
