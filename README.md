# AWS VPC Flow Log module for Terraform [![CircleCI](https://circleci.com/gh/GSA/terraform-vpc-flow-log.svg?style=svg)](https://circleci.com/gh/GSA/terraform-vpc-flow-log)

This is a reusable Terraform module for setting up [VPC flow logs](https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/flow-logs.html) in Amazon Web Services.

## Usage

```hcl
module "flow_logs" {
  source = "github.com/GSA/terraform-vpc-flow-log"
  vpc_id = "${aws_vpc.main.id}"
}
```

See the [optional variables](variables.tf).
