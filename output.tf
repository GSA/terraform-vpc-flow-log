output "log_group_name" {
  description = "The name of the created cloudwatch log group"
  value       = "${aws_flow_log.vpc_flow_log.log_group_name}"
}
