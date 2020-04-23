locals {
  bastion_autoscaling_group_ids     = ["${aws_autoscaling_group.bastions-cs4300-k8s-mycourseindex-com.id}"]
  bastion_security_group_ids        = ["${aws_security_group.bastion-cs4300-k8s-mycourseindex-com.id}"]
  bastions_role_arn                 = "${aws_iam_role.bastions-cs4300-k8s-mycourseindex-com.arn}"
  bastions_role_name                = "${aws_iam_role.bastions-cs4300-k8s-mycourseindex-com.name}"
  cluster_name                      = "cs4300.k8s.mycourseindex.com"
  master_autoscaling_group_ids      = ["${aws_autoscaling_group.master-us-east-1a-masters-cs4300-k8s-mycourseindex-com.id}"]
  master_security_group_ids         = ["${aws_security_group.masters-cs4300-k8s-mycourseindex-com.id}"]
  masters_role_arn                  = "${aws_iam_role.masters-cs4300-k8s-mycourseindex-com.arn}"
  masters_role_name                 = "${aws_iam_role.masters-cs4300-k8s-mycourseindex-com.name}"
  node_autoscaling_group_ids        = ["${aws_autoscaling_group.nodes-cs4300-k8s-mycourseindex-com.id}"]
  node_security_group_ids           = ["${aws_security_group.nodes-cs4300-k8s-mycourseindex-com.id}"]
  node_subnet_ids                   = ["${aws_subnet.us-east-1a-cs4300-k8s-mycourseindex-com.id}"]
  nodes_role_arn                    = "${aws_iam_role.nodes-cs4300-k8s-mycourseindex-com.arn}"
  nodes_role_name                   = "${aws_iam_role.nodes-cs4300-k8s-mycourseindex-com.name}"
  region                            = "us-east-1"
  route_table_private-us-east-1a_id = "${aws_route_table.private-us-east-1a-cs4300-k8s-mycourseindex-com.id}"
  route_table_public_id             = "${aws_route_table.cs4300-k8s-mycourseindex-com.id}"
  subnet_us-east-1a_id              = "${aws_subnet.us-east-1a-cs4300-k8s-mycourseindex-com.id}"
  subnet_utility-us-east-1a_id      = "${aws_subnet.utility-us-east-1a-cs4300-k8s-mycourseindex-com.id}"
  vpc_id                            = "vpc-3adeed40"
}

output "bastion_autoscaling_group_ids" {
  value = ["${aws_autoscaling_group.bastions-cs4300-k8s-mycourseindex-com.id}"]
}

output "bastion_security_group_ids" {
  value = ["${aws_security_group.bastion-cs4300-k8s-mycourseindex-com.id}"]
}

output "bastions_role_arn" {
  value = "${aws_iam_role.bastions-cs4300-k8s-mycourseindex-com.arn}"
}

output "bastions_role_name" {
  value = "${aws_iam_role.bastions-cs4300-k8s-mycourseindex-com.name}"
}

output "cluster_name" {
  value = "cs4300.k8s.mycourseindex.com"
}

output "master_autoscaling_group_ids" {
  value = ["${aws_autoscaling_group.master-us-east-1a-masters-cs4300-k8s-mycourseindex-com.id}"]
}

output "master_security_group_ids" {
  value = ["${aws_security_group.masters-cs4300-k8s-mycourseindex-com.id}"]
}

output "masters_role_arn" {
  value = "${aws_iam_role.masters-cs4300-k8s-mycourseindex-com.arn}"
}

output "masters_role_name" {
  value = "${aws_iam_role.masters-cs4300-k8s-mycourseindex-com.name}"
}

output "node_autoscaling_group_ids" {
  value = ["${aws_autoscaling_group.nodes-cs4300-k8s-mycourseindex-com.id}"]
}

output "node_security_group_ids" {
  value = ["${aws_security_group.nodes-cs4300-k8s-mycourseindex-com.id}"]
}

output "node_subnet_ids" {
  value = ["${aws_subnet.us-east-1a-cs4300-k8s-mycourseindex-com.id}"]
}

output "nodes_role_arn" {
  value = "${aws_iam_role.nodes-cs4300-k8s-mycourseindex-com.arn}"
}

output "nodes_role_name" {
  value = "${aws_iam_role.nodes-cs4300-k8s-mycourseindex-com.name}"
}

output "region" {
  value = "us-east-1"
}

output "route_table_private-us-east-1a_id" {
  value = "${aws_route_table.private-us-east-1a-cs4300-k8s-mycourseindex-com.id}"
}

output "route_table_public_id" {
  value = "${aws_route_table.cs4300-k8s-mycourseindex-com.id}"
}

output "subnet_us-east-1a_id" {
  value = "${aws_subnet.us-east-1a-cs4300-k8s-mycourseindex-com.id}"
}

output "subnet_utility-us-east-1a_id" {
  value = "${aws_subnet.utility-us-east-1a-cs4300-k8s-mycourseindex-com.id}"
}

output "vpc_id" {
  value = "vpc-3adeed40"
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_autoscaling_attachment" "bastions-cs4300-k8s-mycourseindex-com" {
  elb                    = "${aws_elb.bastion-cs4300-k8s-mycourseindex-com.id}"
  autoscaling_group_name = "${aws_autoscaling_group.bastions-cs4300-k8s-mycourseindex-com.id}"
}

resource "aws_autoscaling_attachment" "master-us-east-1a-masters-cs4300-k8s-mycourseindex-com" {
  elb                    = "${aws_elb.api-cs4300-k8s-mycourseindex-com.id}"
  autoscaling_group_name = "${aws_autoscaling_group.master-us-east-1a-masters-cs4300-k8s-mycourseindex-com.id}"
}

resource "aws_autoscaling_group" "bastions-cs4300-k8s-mycourseindex-com" {
  name                 = "bastions.cs4300.k8s.mycourseindex.com"
  launch_configuration = "${aws_launch_configuration.bastions-cs4300-k8s-mycourseindex-com.id}"
  max_size             = 1
  min_size             = 1
  vpc_zone_identifier  = ["${aws_subnet.utility-us-east-1a-cs4300-k8s-mycourseindex-com.id}"]

  tags = [
    {
      key                 = "KubernetesCluster"
      value               = "cs4300.k8s.mycourseindex.com"
      propagate_at_launch = true
    },
    {
      key                 = "Name"
      value               = "bastions.cs4300.k8s.mycourseindex.com"
      propagate_at_launch = true
    },
    {
      key                 = "k8s.io/cluster-autoscaler/node-template/label/kops.k8s.io/instancegroup"
      value               = "bastions"
      propagate_at_launch = true
    },
    {
      key                 = "k8s.io/role/bastion"
      value               = "1"
      propagate_at_launch = true
    },
    {
      key                 = "kops.k8s.io/instancegroup"
      value               = "bastions"
      propagate_at_launch = true
    }
  ]

  metrics_granularity = "1Minute"
  enabled_metrics     = ["GroupDesiredCapacity", "GroupInServiceInstances", "GroupMaxSize", "GroupMinSize", "GroupPendingInstances", "GroupStandbyInstances", "GroupTerminatingInstances", "GroupTotalInstances"]
}

resource "aws_autoscaling_group" "master-us-east-1a-masters-cs4300-k8s-mycourseindex-com" {
  name                 = "master-us-east-1a.masters.cs4300.k8s.mycourseindex.com"
  launch_configuration = "${aws_launch_configuration.master-us-east-1a-masters-cs4300-k8s-mycourseindex-com.id}"
  max_size             = 1
  min_size             = 1
  vpc_zone_identifier  = ["${aws_subnet.us-east-1a-cs4300-k8s-mycourseindex-com.id}"]

  tags = [
    {
      key                 = "KubernetesCluster"
      value               = "cs4300.k8s.mycourseindex.com"
      propagate_at_launch = true
    },
    {
      key                 = "Name"
      value               = "master-us-east-1a.masters.cs4300.k8s.mycourseindex.com"
      propagate_at_launch = true
    },
    {
      key                 = "k8s.io/cluster-autoscaler/node-template/label/kops.k8s.io/instancegroup"
      value               = "master-us-east-1a"
      propagate_at_launch = true
    },
    {
      key                 = "k8s.io/role/master"
      value               = "1"
      propagate_at_launch = true
    },
    {
      key                 = "kops.k8s.io/instancegroup"
      value               = "master-us-east-1a"
      propagate_at_launch = true
    }
  ]
  metrics_granularity = "1Minute"
  enabled_metrics     = ["GroupDesiredCapacity", "GroupInServiceInstances", "GroupMaxSize", "GroupMinSize", "GroupPendingInstances", "GroupStandbyInstances", "GroupTerminatingInstances", "GroupTotalInstances"]
}

resource "aws_autoscaling_group" "nodes-cs4300-k8s-mycourseindex-com" {
  name                 = "nodes.cs4300.k8s.mycourseindex.com"
  launch_configuration = "${aws_launch_configuration.nodes-cs4300-k8s-mycourseindex-com.id}"
  max_size             = 1
  min_size             = 1
  vpc_zone_identifier  = ["${aws_subnet.us-east-1a-cs4300-k8s-mycourseindex-com.id}"]

  tags = [
    {
      key                 = "KubernetesCluster"
      value               = "cs4300.k8s.mycourseindex.com"
      propagate_at_launch = true
    },
    {
      key                 = "Name"
      value               = "nodes.cs4300.k8s.mycourseindex.com"
      propagate_at_launch = true
    },
    {
      key                 = "k8s.io/cluster-autoscaler/node-template/label/kops.k8s.io/instancegroup"
      value               = "nodes"
      propagate_at_launch = true
    },
    {
      key                 = "k8s.io/role/node"
      value               = "1"
      propagate_at_launch = true
    },
    {
      key                 = "kops.k8s.io/instancegroup"
      value               = "nodes"
      propagate_at_launch = true
    }
  ]

  metrics_granularity = "1Minute"
  enabled_metrics     = ["GroupDesiredCapacity", "GroupInServiceInstances", "GroupMaxSize", "GroupMinSize", "GroupPendingInstances", "GroupStandbyInstances", "GroupTerminatingInstances", "GroupTotalInstances"]
}

resource "aws_ebs_volume" "a-etcd-events-cs4300-k8s-mycourseindex-com" {
  availability_zone = "us-east-1a"
  size              = 20
  type              = "gp2"
  encrypted         = false

  tags = {
    KubernetesCluster                                    = "cs4300.k8s.mycourseindex.com"
    Name                                                 = "a.etcd-events.cs4300.k8s.mycourseindex.com"
    "k8s.io/etcd/events"                                 = "a/a"
    "k8s.io/role/master"                                 = "1"
    "kubernetes.io/cluster/cs4300.k8s.mycourseindex.com" = "owned"
  }
}

resource "aws_ebs_volume" "a-etcd-main-cs4300-k8s-mycourseindex-com" {
  availability_zone = "us-east-1a"
  size              = 20
  type              = "gp2"
  encrypted         = false

  tags = {
    KubernetesCluster                                    = "cs4300.k8s.mycourseindex.com"
    Name                                                 = "a.etcd-main.cs4300.k8s.mycourseindex.com"
    "k8s.io/etcd/main"                                   = "a/a"
    "k8s.io/role/master"                                 = "1"
    "kubernetes.io/cluster/cs4300.k8s.mycourseindex.com" = "owned"
  }
}

resource "aws_eip" "us-east-1a-cs4300-k8s-mycourseindex-com" {
  vpc = true

  tags = {
    KubernetesCluster                                    = "cs4300.k8s.mycourseindex.com"
    Name                                                 = "us-east-1a.cs4300.k8s.mycourseindex.com"
    "kubernetes.io/cluster/cs4300.k8s.mycourseindex.com" = "owned"
  }
}

resource "aws_elb" "api-cs4300-k8s-mycourseindex-com" {
  name = "api-cs4300-k8s-mycoursein-g8s083"

  listener {
    instance_port     = 443
    instance_protocol = "TCP"
    lb_port           = 443
    lb_protocol       = "TCP"
  }

  security_groups = ["${aws_security_group.api-elb-cs4300-k8s-mycourseindex-com.id}"]
  subnets         = ["${aws_subnet.utility-us-east-1a-cs4300-k8s-mycourseindex-com.id}"]

  health_check {
    target              = "SSL:443"
    healthy_threshold   = 2
    unhealthy_threshold = 2
    interval            = 10
    timeout             = 5
  }

  cross_zone_load_balancing = false
  idle_timeout              = 300

  tags = {
    KubernetesCluster                                    = "cs4300.k8s.mycourseindex.com"
    Name                                                 = "api.cs4300.k8s.mycourseindex.com"
    "kubernetes.io/cluster/cs4300.k8s.mycourseindex.com" = "owned"
  }
}

resource "aws_elb" "bastion-cs4300-k8s-mycourseindex-com" {
  name = "bastion-cs4300-k8s-mycour-1k3tu1"

  listener {
    instance_port     = 22
    instance_protocol = "TCP"
    lb_port           = 22
    lb_protocol       = "TCP"
  }

  security_groups = ["${aws_security_group.bastion-elb-cs4300-k8s-mycourseindex-com.id}"]
  subnets         = ["${aws_subnet.utility-us-east-1a-cs4300-k8s-mycourseindex-com.id}"]

  health_check {
    target              = "TCP:22"
    healthy_threshold   = 2
    unhealthy_threshold = 2
    interval            = 10
    timeout             = 5
  }

  idle_timeout = 300

  tags = {
    KubernetesCluster                                    = "cs4300.k8s.mycourseindex.com"
    Name                                                 = "bastion.cs4300.k8s.mycourseindex.com"
    "kubernetes.io/cluster/cs4300.k8s.mycourseindex.com" = "owned"
  }
}

resource "aws_iam_instance_profile" "bastions-cs4300-k8s-mycourseindex-com" {
  name = "bastions.cs4300.k8s.mycourseindex.com"
  role = "${aws_iam_role.bastions-cs4300-k8s-mycourseindex-com.name}"
}

resource "aws_iam_instance_profile" "masters-cs4300-k8s-mycourseindex-com" {
  name = "masters.cs4300.k8s.mycourseindex.com"
  role = "${aws_iam_role.masters-cs4300-k8s-mycourseindex-com.name}"
}

resource "aws_iam_instance_profile" "nodes-cs4300-k8s-mycourseindex-com" {
  name = "nodes.cs4300.k8s.mycourseindex.com"
  role = "${aws_iam_role.nodes-cs4300-k8s-mycourseindex-com.name}"
}

resource "aws_iam_role" "bastions-cs4300-k8s-mycourseindex-com" {
  name               = "bastions.cs4300.k8s.mycourseindex.com"
  assume_role_policy = "${file("${path.module}/data/aws_iam_role_bastions.cs4300.k8s.mycourseindex.com_policy")}"
}

resource "aws_iam_role" "masters-cs4300-k8s-mycourseindex-com" {
  name               = "masters.cs4300.k8s.mycourseindex.com"
  assume_role_policy = "${file("${path.module}/data/aws_iam_role_masters.cs4300.k8s.mycourseindex.com_policy")}"
}

resource "aws_iam_role" "nodes-cs4300-k8s-mycourseindex-com" {
  name               = "nodes.cs4300.k8s.mycourseindex.com"
  assume_role_policy = "${file("${path.module}/data/aws_iam_role_nodes.cs4300.k8s.mycourseindex.com_policy")}"
}

resource "aws_iam_role_policy" "bastions-cs4300-k8s-mycourseindex-com" {
  name   = "bastions.cs4300.k8s.mycourseindex.com"
  role   = "${aws_iam_role.bastions-cs4300-k8s-mycourseindex-com.name}"
  policy = "${file("${path.module}/data/aws_iam_role_policy_bastions.cs4300.k8s.mycourseindex.com_policy")}"
}

resource "aws_iam_role_policy" "masters-cs4300-k8s-mycourseindex-com" {
  name   = "masters.cs4300.k8s.mycourseindex.com"
  role   = "${aws_iam_role.masters-cs4300-k8s-mycourseindex-com.name}"
  policy = "${file("${path.module}/data/aws_iam_role_policy_masters.cs4300.k8s.mycourseindex.com_policy")}"
}

resource "aws_iam_role_policy" "nodes-cs4300-k8s-mycourseindex-com" {
  name   = "nodes.cs4300.k8s.mycourseindex.com"
  role   = "${aws_iam_role.nodes-cs4300-k8s-mycourseindex-com.name}"
  policy = "${file("${path.module}/data/aws_iam_role_policy_nodes.cs4300.k8s.mycourseindex.com_policy")}"
}

resource "aws_key_pair" "kubernetes-cs4300-k8s-mycourseindex-com-fd3242d36d41c1c3901c47795ec774a6" {
  key_name   = "kubernetes.cs4300.k8s.mycourseindex.com-fd:32:42:d3:6d:41:c1:c3:90:1c:47:79:5e:c7:74:a6"
  public_key = "${file("${path.module}/data/aws_key_pair_kubernetes.cs4300.k8s.mycourseindex.com-fd3242d36d41c1c3901c47795ec774a6_public_key")}"
}

resource "aws_launch_configuration" "bastions-cs4300-k8s-mycourseindex-com" {
  name_prefix                 = "bastions.cs4300.k8s.mycourseindex.com-"
  image_id                    = "ami-0938c52697eb48ee2"
  instance_type               = "t2.micro"
  key_name                    = "${aws_key_pair.kubernetes-cs4300-k8s-mycourseindex-com-fd3242d36d41c1c3901c47795ec774a6.id}"
  iam_instance_profile        = "${aws_iam_instance_profile.bastions-cs4300-k8s-mycourseindex-com.id}"
  security_groups             = ["${aws_security_group.bastion-cs4300-k8s-mycourseindex-com.id}"]
  associate_public_ip_address = true

  root_block_device {
    volume_type           = "gp2"
    volume_size           = 32
    delete_on_termination = true
  }

  lifecycle {
    create_before_destroy = true
  }

  enable_monitoring = false
}

resource "aws_launch_configuration" "master-us-east-1a-masters-cs4300-k8s-mycourseindex-com" {
  name_prefix                 = "master-us-east-1a.masters.cs4300.k8s.mycourseindex.com-"
  image_id                    = "ami-0938c52697eb48ee2"
  instance_type               = "t3.medium"
  key_name                    = "${aws_key_pair.kubernetes-cs4300-k8s-mycourseindex-com-fd3242d36d41c1c3901c47795ec774a6.id}"
  iam_instance_profile        = "${aws_iam_instance_profile.masters-cs4300-k8s-mycourseindex-com.id}"
  security_groups             = ["${aws_security_group.masters-cs4300-k8s-mycourseindex-com.id}"]
  associate_public_ip_address = false
  user_data                   = "${file("${path.module}/data/aws_launch_configuration_master-us-east-1a.masters.cs4300.k8s.mycourseindex.com_user_data")}"

  root_block_device {
    volume_type           = "gp2"
    volume_size           = 64
    delete_on_termination = true
  }

  lifecycle {
    create_before_destroy = true
  }

  enable_monitoring = false
}

resource "aws_launch_configuration" "nodes-cs4300-k8s-mycourseindex-com" {
  name_prefix                 = "nodes.cs4300.k8s.mycourseindex.com-"
  image_id                    = "ami-0938c52697eb48ee2"
  instance_type               = "t3.2xlarge"
  key_name                    = "${aws_key_pair.kubernetes-cs4300-k8s-mycourseindex-com-fd3242d36d41c1c3901c47795ec774a6.id}"
  iam_instance_profile        = "${aws_iam_instance_profile.nodes-cs4300-k8s-mycourseindex-com.id}"
  security_groups             = ["${aws_security_group.nodes-cs4300-k8s-mycourseindex-com.id}"]
  associate_public_ip_address = false
  user_data                   = "${file("${path.module}/data/aws_launch_configuration_nodes.cs4300.k8s.mycourseindex.com_user_data")}"

  root_block_device {
    volume_type           = "gp2"
    volume_size           = 128
    delete_on_termination = true
  }

  lifecycle {
    create_before_destroy = true
  }

  enable_monitoring = false
}

resource "aws_nat_gateway" "us-east-1a-cs4300-k8s-mycourseindex-com" {
  allocation_id = "${aws_eip.us-east-1a-cs4300-k8s-mycourseindex-com.id}"
  subnet_id     = "${aws_subnet.utility-us-east-1a-cs4300-k8s-mycourseindex-com.id}"

  tags = {
    KubernetesCluster                                    = "cs4300.k8s.mycourseindex.com"
    Name                                                 = "us-east-1a.cs4300.k8s.mycourseindex.com"
    "kubernetes.io/cluster/cs4300.k8s.mycourseindex.com" = "owned"
  }
}

resource "aws_route" "default-0-0-0-0--0" {
  route_table_id         = "${aws_route_table.cs4300-k8s-mycourseindex-com.id}"
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = "igw-3ea2c445"
}

resource "aws_route" "private-us-east-1a-0-0-0-0--0" {
  route_table_id         = "${aws_route_table.private-us-east-1a-cs4300-k8s-mycourseindex-com.id}"
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = "${aws_nat_gateway.us-east-1a-cs4300-k8s-mycourseindex-com.id}"
}

resource "aws_route53_record" "api-cs4300-k8s-mycourseindex-com" {
  name = "api.cs4300.k8s.mycourseindex.com"
  type = "A"

  alias {
    name                   = "${aws_elb.api-cs4300-k8s-mycourseindex-com.dns_name}"
    zone_id                = "${aws_elb.api-cs4300-k8s-mycourseindex-com.zone_id}"
    evaluate_target_health = false
  }

  zone_id = "/hostedzone/ZXNZ3MUU52AOY"
}

resource "aws_route53_record" "bastion-cs4300-k8s-mycourseindex-com" {
  name = "bastion.cs4300.k8s.mycourseindex.com"
  type = "A"

  alias {
    name                   = "${aws_elb.bastion-cs4300-k8s-mycourseindex-com.dns_name}"
    zone_id                = "${aws_elb.bastion-cs4300-k8s-mycourseindex-com.zone_id}"
    evaluate_target_health = false
  }

  zone_id = "/hostedzone/ZXNZ3MUU52AOY"
}

resource "aws_route_table" "cs4300-k8s-mycourseindex-com" {
  vpc_id = "vpc-3adeed40"

  tags = {
    KubernetesCluster                                    = "cs4300.k8s.mycourseindex.com"
    Name                                                 = "cs4300.k8s.mycourseindex.com"
    "kubernetes.io/cluster/cs4300.k8s.mycourseindex.com" = "owned"
    "kubernetes.io/kops/role"                            = "public"
  }
}

resource "aws_route_table" "private-us-east-1a-cs4300-k8s-mycourseindex-com" {
  vpc_id = "vpc-3adeed40"

  tags = {
    KubernetesCluster                                    = "cs4300.k8s.mycourseindex.com"
    Name                                                 = "private-us-east-1a.cs4300.k8s.mycourseindex.com"
    "kubernetes.io/cluster/cs4300.k8s.mycourseindex.com" = "owned"
    "kubernetes.io/kops/role"                            = "private-us-east-1a"
  }
}

resource "aws_route_table_association" "private-us-east-1a-cs4300-k8s-mycourseindex-com" {
  subnet_id      = "${aws_subnet.us-east-1a-cs4300-k8s-mycourseindex-com.id}"
  route_table_id = "${aws_route_table.private-us-east-1a-cs4300-k8s-mycourseindex-com.id}"
}

resource "aws_route_table_association" "utility-us-east-1a-cs4300-k8s-mycourseindex-com" {
  subnet_id      = "${aws_subnet.utility-us-east-1a-cs4300-k8s-mycourseindex-com.id}"
  route_table_id = "${aws_route_table.cs4300-k8s-mycourseindex-com.id}"
}

resource "aws_security_group" "api-elb-cs4300-k8s-mycourseindex-com" {
  name        = "api-elb.cs4300.k8s.mycourseindex.com"
  vpc_id      = "vpc-3adeed40"
  description = "Security group for api ELB"

  tags = {
    KubernetesCluster                                    = "cs4300.k8s.mycourseindex.com"
    Name                                                 = "api-elb.cs4300.k8s.mycourseindex.com"
    "kubernetes.io/cluster/cs4300.k8s.mycourseindex.com" = "owned"
  }
}

resource "aws_security_group" "bastion-cs4300-k8s-mycourseindex-com" {
  name        = "bastion.cs4300.k8s.mycourseindex.com"
  vpc_id      = "vpc-3adeed40"
  description = "Security group for bastion"

  tags = {
    KubernetesCluster                                    = "cs4300.k8s.mycourseindex.com"
    Name                                                 = "bastion.cs4300.k8s.mycourseindex.com"
    "kubernetes.io/cluster/cs4300.k8s.mycourseindex.com" = "owned"
  }
}

resource "aws_security_group" "bastion-elb-cs4300-k8s-mycourseindex-com" {
  name        = "bastion-elb.cs4300.k8s.mycourseindex.com"
  vpc_id      = "vpc-3adeed40"
  description = "Security group for bastion ELB"

  tags = {
    KubernetesCluster                                    = "cs4300.k8s.mycourseindex.com"
    Name                                                 = "bastion-elb.cs4300.k8s.mycourseindex.com"
    "kubernetes.io/cluster/cs4300.k8s.mycourseindex.com" = "owned"
  }
}

resource "aws_security_group" "masters-cs4300-k8s-mycourseindex-com" {
  name        = "masters.cs4300.k8s.mycourseindex.com"
  vpc_id      = "vpc-3adeed40"
  description = "Security group for masters"

  tags = {
    KubernetesCluster                                    = "cs4300.k8s.mycourseindex.com"
    Name                                                 = "masters.cs4300.k8s.mycourseindex.com"
    "kubernetes.io/cluster/cs4300.k8s.mycourseindex.com" = "owned"
  }
}

resource "aws_security_group" "nodes-cs4300-k8s-mycourseindex-com" {
  name        = "nodes.cs4300.k8s.mycourseindex.com"
  vpc_id      = "vpc-3adeed40"
  description = "Security group for nodes"

  tags = {
    KubernetesCluster                                    = "cs4300.k8s.mycourseindex.com"
    Name                                                 = "nodes.cs4300.k8s.mycourseindex.com"
    "kubernetes.io/cluster/cs4300.k8s.mycourseindex.com" = "owned"
  }
}

resource "aws_security_group_rule" "all-master-to-master" {
  type                     = "ingress"
  security_group_id        = "${aws_security_group.masters-cs4300-k8s-mycourseindex-com.id}"
  source_security_group_id = "${aws_security_group.masters-cs4300-k8s-mycourseindex-com.id}"
  from_port                = 0
  to_port                  = 0
  protocol                 = "-1"
}

resource "aws_security_group_rule" "all-master-to-node" {
  type                     = "ingress"
  security_group_id        = "${aws_security_group.nodes-cs4300-k8s-mycourseindex-com.id}"
  source_security_group_id = "${aws_security_group.masters-cs4300-k8s-mycourseindex-com.id}"
  from_port                = 0
  to_port                  = 0
  protocol                 = "-1"
}

resource "aws_security_group_rule" "all-node-to-node" {
  type                     = "ingress"
  security_group_id        = "${aws_security_group.nodes-cs4300-k8s-mycourseindex-com.id}"
  source_security_group_id = "${aws_security_group.nodes-cs4300-k8s-mycourseindex-com.id}"
  from_port                = 0
  to_port                  = 0
  protocol                 = "-1"
}

resource "aws_security_group_rule" "api-elb-egress" {
  type              = "egress"
  security_group_id = "${aws_security_group.api-elb-cs4300-k8s-mycourseindex-com.id}"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "bastion-egress" {
  type              = "egress"
  security_group_id = "${aws_security_group.bastion-cs4300-k8s-mycourseindex-com.id}"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "bastion-elb-egress" {
  type              = "egress"
  security_group_id = "${aws_security_group.bastion-elb-cs4300-k8s-mycourseindex-com.id}"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "bastion-to-master-ssh" {
  type                     = "ingress"
  security_group_id        = "${aws_security_group.masters-cs4300-k8s-mycourseindex-com.id}"
  source_security_group_id = "${aws_security_group.bastion-cs4300-k8s-mycourseindex-com.id}"
  from_port                = 22
  to_port                  = 22
  protocol                 = "tcp"
}

resource "aws_security_group_rule" "bastion-to-node-ssh" {
  type                     = "ingress"
  security_group_id        = "${aws_security_group.nodes-cs4300-k8s-mycourseindex-com.id}"
  source_security_group_id = "${aws_security_group.bastion-cs4300-k8s-mycourseindex-com.id}"
  from_port                = 22
  to_port                  = 22
  protocol                 = "tcp"
}

resource "aws_security_group_rule" "https-api-elb-0-0-0-0--0" {
  type              = "ingress"
  security_group_id = "${aws_security_group.api-elb-cs4300-k8s-mycourseindex-com.id}"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "https-elb-to-master" {
  type                     = "ingress"
  security_group_id        = "${aws_security_group.masters-cs4300-k8s-mycourseindex-com.id}"
  source_security_group_id = "${aws_security_group.api-elb-cs4300-k8s-mycourseindex-com.id}"
  from_port                = 443
  to_port                  = 443
  protocol                 = "tcp"
}

resource "aws_security_group_rule" "icmp-pmtu-api-elb-0-0-0-0--0" {
  type              = "ingress"
  security_group_id = "${aws_security_group.api-elb-cs4300-k8s-mycourseindex-com.id}"
  from_port         = 3
  to_port           = 4
  protocol          = "icmp"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "master-egress" {
  type              = "egress"
  security_group_id = "${aws_security_group.masters-cs4300-k8s-mycourseindex-com.id}"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "node-egress" {
  type              = "egress"
  security_group_id = "${aws_security_group.nodes-cs4300-k8s-mycourseindex-com.id}"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "node-to-master-protocol-ipip" {
  type                     = "ingress"
  security_group_id        = "${aws_security_group.masters-cs4300-k8s-mycourseindex-com.id}"
  source_security_group_id = "${aws_security_group.nodes-cs4300-k8s-mycourseindex-com.id}"
  from_port                = 0
  to_port                  = 65535
  protocol                 = "4"
}

resource "aws_security_group_rule" "node-to-master-tcp-1-2379" {
  type                     = "ingress"
  security_group_id        = "${aws_security_group.masters-cs4300-k8s-mycourseindex-com.id}"
  source_security_group_id = "${aws_security_group.nodes-cs4300-k8s-mycourseindex-com.id}"
  from_port                = 1
  to_port                  = 2379
  protocol                 = "tcp"
}

resource "aws_security_group_rule" "node-to-master-tcp-2382-4001" {
  type                     = "ingress"
  security_group_id        = "${aws_security_group.masters-cs4300-k8s-mycourseindex-com.id}"
  source_security_group_id = "${aws_security_group.nodes-cs4300-k8s-mycourseindex-com.id}"
  from_port                = 2382
  to_port                  = 4001
  protocol                 = "tcp"
}

resource "aws_security_group_rule" "node-to-master-tcp-4003-65535" {
  type                     = "ingress"
  security_group_id        = "${aws_security_group.masters-cs4300-k8s-mycourseindex-com.id}"
  source_security_group_id = "${aws_security_group.nodes-cs4300-k8s-mycourseindex-com.id}"
  from_port                = 4003
  to_port                  = 65535
  protocol                 = "tcp"
}

resource "aws_security_group_rule" "node-to-master-udp-1-65535" {
  type                     = "ingress"
  security_group_id        = "${aws_security_group.masters-cs4300-k8s-mycourseindex-com.id}"
  source_security_group_id = "${aws_security_group.nodes-cs4300-k8s-mycourseindex-com.id}"
  from_port                = 1
  to_port                  = 65535
  protocol                 = "udp"
}

resource "aws_security_group_rule" "ssh-elb-to-bastion" {
  type                     = "ingress"
  security_group_id        = "${aws_security_group.bastion-cs4300-k8s-mycourseindex-com.id}"
  source_security_group_id = "${aws_security_group.bastion-elb-cs4300-k8s-mycourseindex-com.id}"
  from_port                = 22
  to_port                  = 22
  protocol                 = "tcp"
}

resource "aws_security_group_rule" "ssh-external-to-bastion-elb-0-0-0-0--0" {
  type              = "ingress"
  security_group_id = "${aws_security_group.bastion-elb-cs4300-k8s-mycourseindex-com.id}"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_subnet" "us-east-1a-cs4300-k8s-mycourseindex-com" {
  vpc_id            = "vpc-3adeed40"
  cidr_block        = "172.31.224.0/19"
  availability_zone = "us-east-1a"

  tags = {
    KubernetesCluster                                    = "cs4300.k8s.mycourseindex.com"
    Name                                                 = "us-east-1a.cs4300.k8s.mycourseindex.com"
    SubnetType                                           = "Private"
    "kubernetes.io/cluster/cs4300.k8s.mycourseindex.com" = "owned"
    "kubernetes.io/role/internal-elb"                    = "1"
  }
}

resource "aws_subnet" "utility-us-east-1a-cs4300-k8s-mycourseindex-com" {
  vpc_id            = "vpc-3adeed40"
  cidr_block        = "172.31.128.0/22"
  availability_zone = "us-east-1a"

  tags = {
    KubernetesCluster                                    = "cs4300.k8s.mycourseindex.com"
    Name                                                 = "utility-us-east-1a.cs4300.k8s.mycourseindex.com"
    SubnetType                                           = "Utility"
    "kubernetes.io/cluster/cs4300.k8s.mycourseindex.com" = "owned"
    "kubernetes.io/role/elb"                             = "1"
  }
}

terraform {
  required_version = ">= 0.9.3"
}
