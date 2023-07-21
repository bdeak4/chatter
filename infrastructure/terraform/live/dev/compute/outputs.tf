output "app_eips" {
  value = module.ec2_app.eips
}

output "app_instance_ids" {
  value = module.ec2_app.ids
}
