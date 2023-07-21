variable "infra_env" {
  type        = string
  description = "infrastructure environment"
}

variable "infra_role" {
  type        = string
  description = "infrastructure purpose"
}

variable "instance_count" {
  type        = number
  description = "number of instances to create"
  default     = 1
}

variable "instance_type" {
  type        = string
  description = "instance type"
  default     = "t3a.micro"
}

variable "instance_root_device_size" {
  type        = number
  description = "Root bock device size in GB"
  default     = 12
}

variable "subnets" {
  type        = list(string)
  description = "valid subnets to assign to server"
}

variable "security_groups" {
  type        = list(string)
  description = "security groups to assign to server"
  default     = []
}

variable "key_pair" {
  type        = string
  description = "key pair name"
  default     = null
}

variable "create_eip" {
  type        = bool
  default     = false
  description = "whether or create an EIP for the ec2 instances or not"
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "tags for the ec2 instance"
}
