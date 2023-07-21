resource "random_shuffle" "subnets" {
  input        = var.subnets
  result_count = var.instance_count
}

resource "aws_instance" "instance" {
  ami                    = data.aws_ami.debian.id
  instance_type          = var.instance_type
  monitoring             = true
  key_name               = var.key_pair
  vpc_security_group_ids = var.security_groups
  subnet_id              = random_shuffle.subnets.result[count.index]
  count                  = var.instance_count

  root_block_device {
    volume_type           = "gp2"
    volume_size           = var.instance_root_device_size
    delete_on_termination = true
  }

  tags = merge(
    {
      Name        = "chatter-${var.infra_role}-${var.infra_env}-${count.index + 1}"
      Project     = "chatter"
      Role        = var.infra_role
      Environment = var.infra_env
      ManagedBy   = "terraform"
    },
    var.tags
  )
}

resource "aws_eip" "eip" {
  count = (var.create_eip) ? var.instance_count : 0

  tags = {
    Name        = "chatter-${var.infra_role}-address-${var.infra_env}-${count.index + 1}"
    Project     = "chatter"
    Role        = var.infra_role
    Environment = var.infra_env
    ManagedBy   = "terraform"
  }
}

resource "aws_eip_association" "eip_assoc" {
  count         = (var.create_eip) ? var.instance_count : 0
  instance_id   = aws_instance.instance[count.index].id
  allocation_id = aws_eip.eip[count.index].id
}
