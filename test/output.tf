output "log_group_name" {
  value = "${module.flow_logs.log_group_name}"
}

output "ip" {
  value = "${aws_eip.main.public_ip}"
}
