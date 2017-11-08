variable "vpc_id" {}

variable "prefix" {
  description = "The prefix for the resource names. You will probably want to set this to the name of your VPC, if you have multiple."
  default = "vpc"
}
