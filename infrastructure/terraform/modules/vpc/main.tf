module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.0"

  name             = "chatter-${var.infra_env}-vpc"
  cidr             = var.vpc_cidr
  azs              = var.azs
  private_subnets  = var.private_subnets
  public_subnets   = var.public_subnets
  database_subnets = var.database_subnets

  # Single NAT Gateway
  # enable_nat_gateway     = true
  # single_nat_gateway     = true
  # one_nat_gateway_per_az = false
  enable_nat_gateway = false

  tags = {
    Name        = "chatter-${var.infra_env}-vpc"
    Project     = "chatter"
    Environment = var.infra_env
    ManagedBy   = "terraform"
  }

  public_subnet_tags = {
    Role = "public"
  }

  private_subnet_tags = {
    Role = "private"
  }

  database_subnet_tags = {
    Role = "database"
  }
}

