data "aws_subnets" "public_subnets" {
  tags = {
    Name        = "chatter-${var.infra_env}-vpc"
    Project     = "chatter"
    Environment = var.infra_env
    ManagedBy   = "terraform"
    Role        = "public"
  }
}

data "aws_security_groups" "public_sg" {
  tags = {
    Name        = "chatter-${var.infra_env}-public-sg"
    Project     = "chatter"
    Role        = "public"
    Environment = var.infra_env
    ManagedBy   = "terraform"
  }
}
