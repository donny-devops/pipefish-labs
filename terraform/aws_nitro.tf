# PipeFish Labs — AWS Nitro Enclave Compute Instance Infrastructure
# Enables hardware-isolated RAM-only execution for Zero-Data Retention (ZDR)

resource "aws_instance" "nitro_enclave_node" {
  ami           = "ami-0c7217cdde317cfec" # Amazon Linux 2023 Enclave-optimized
  instance_type = var.enclave_instance_type

  enclave_options {
    enabled = true
  }

  vpc_security_group_ids = [aws_security_group.mesh_sg.id]

  root_block_device {
    encrypted   = true
    kms_key_id  = aws_kms_key.enclave_pqc_kms_key.arn
    volume_type = "gp3"
    volume_size = 50
  }

  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required" # IMDSv2 strictly enforced
    http_put_response_hop_limit = 1
  }

  tags = {
    Name        = "${var.cluster_name}-nitro-node"
    Enclave     = "Enabled"
    SecurityZDR = "Strict"
  }
}
