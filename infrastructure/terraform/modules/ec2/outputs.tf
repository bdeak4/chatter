output "eips" {
  value = aws_eip.eip[*].public_ip
}

output "ids" {
  value = aws_instance.instance[*].id
}
