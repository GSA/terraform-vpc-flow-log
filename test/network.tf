data "aws_region" "current" {
  current = true
}

module "network" {
  source = "terraform-aws-modules/vpc/aws"
  version = "~> 1.0"

  name = "terraform-vpc-flow-log-test"
  azs = ["${data.aws_region.current.name}d"]
  cidr = "10.0.0.0/16"
  public_subnets = ["10.0.1.0/24"]
  enable_nat_gateway = true
}

module "flow_logs" {
  source = "../"
  vpc_id = "${module.network.vpc_id}"
  prefix = "${var.prefix}"
}
