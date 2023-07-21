terraform {
  required_version = ">= 1.0.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "chatter-tfstate"
    dynamodb_table = "chatter-tfstate"
    region         = "us-east-1"
    profile        = "chatter"
    encrypt        = true
  }
}

provider "aws" {
  profile = "chatter"
  region  = "eu-central-1"
}

locals {
  cidr_subnets = cidrsubnets("10.0.0.0/17", 4, 4, 4, 4, 4, 4, 4, 4, 4)
}

module "vpc" {
  source = "../../../modules/vpc"

  infra_env      = var.infra_env
  vpc_cidr       = "10.0.0.0/17"
  azs            = ["eu-central-1a", "eu-central-1b", "eu-central-1c"]
  public_subnets = slice(local.cidr_subnets, 0, 3)
  # private_subnets  = slice(local.cidr_subnets, 3, 6)
  # database_subnets = slice(local.cidr_subnets, 6, 9)
}
