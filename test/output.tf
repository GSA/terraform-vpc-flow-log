output "log_group_name" {
  value = "${module.flow_logs.log_group_name}"
}

output "ip" {
  value = "${aws_instance.main.public_ip}"
}
