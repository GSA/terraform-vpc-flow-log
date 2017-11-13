resource "aws_network_interface" "test" {
  subnet_id       = "${module.network.public_subnets[0]}"
  security_groups = ["${module.network.default_security_group_id}"]
}

resource "aws_eip" "main" {
  vpc                       = true
  network_interface         = "${aws_network_interface.test.id}"
}
