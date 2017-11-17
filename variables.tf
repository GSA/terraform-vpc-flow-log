variable "vpc_id" {}

variable "prefix" {
  description = "The prefix for the resource names. You will probably want to set this to the name of your VPC, if you have multiple."
  default = "vpc"
}

variable "traffic_type" {
  default = "ALL"
  description = "https://www.terraform.io/docs/providers/aws/r/flow_log.html#traffic_type"
}

// workaround for not being able to do interpolation in variable defaults
// https://github.com/hashicorp/terraform/issues/4084
locals {
  default_log_group_name = "${var.prefix}-flow-log"
}
variable "log_group_name" {
  default = ""
  description = "Defaults to `$${default_log_group_name}`"
}
