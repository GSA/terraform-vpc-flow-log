resource "aws_key_pair" "deployer" {
  key_name_prefix = "${var.prefix}-deployer-key"
  public_key = "${file("~/.ssh/id_rsa.pub")}"
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_security_group" "main" {
  vpc_id = "${module.network.vpc_id}"

  # SSH access from anywhere
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "main" {
  ami           = "${data.aws_ami.ubuntu.id}"
  instance_type = "t2.micro"

  subnet_id = "${module.network.public_subnets[0]}"
  vpc_security_group_ids = ["${aws_security_group.main.id}"]

  key_name = "${aws_key_pair.deployer.key_name}"

  provisioner "remote-exec" {
    inline = ["echo Successfully connected"]

    connection {
      user = "ubuntu"
    }
  }
}
