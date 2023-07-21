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

module "ec2_app" {
  source = "../../../modules/ec2"

  infra_env       = var.infra_env
  infra_role      = "web"
  instance_count  = 2
  subnets         = data.aws_subnets.public_subnets.ids
  security_groups = data.aws_security_groups.public_sg.ids
  create_eip      = true
}
