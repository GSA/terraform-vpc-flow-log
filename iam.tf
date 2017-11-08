data "template_file" "assume_role_policy" {
  template = "${file("${path.module}/assume_role_policy.json")}"
}

data "template_file" "log_policy" {
  template = "${file("${path.module}/log_policy.json")}"
}

resource "aws_cloudwatch_log_group" "flow_log_group" {
  name = "${var.vpc_name}-flow-log"
}

resource "aws_iam_role" "iam_log_role" {
  name = "${var.vpc_name}-flow-log-role"
  assume_role_policy = "${data.template_file.assume_role_policy.rendered}"
}

resource "aws_iam_role_policy" "log_policy" {
  name = "${var.vpc_name}-flow-log-policy"
  role = "${aws_iam_role.iam_log_role.id}"
  policy = "${data.template_file.log_policy.rendered}"
}
