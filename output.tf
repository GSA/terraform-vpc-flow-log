output "log_group_name" {
  value = "${aws_flow_log.vpc_flow_log.log_group_name}"
}
