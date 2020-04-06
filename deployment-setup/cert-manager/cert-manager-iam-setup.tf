resource "aws_iam_role" "cert_manager_pod_role" {
  name               = "cert_manager_pod_role"
  assume_role_policy = "${file("pod-role-trust-policy.json")}"
}

resource "aws_iam_role_policy" "cert_manager_pod_role_policy" {
  name   = "cert_manager_pod_role_policy"
  role   = "${aws_iam_role.cert_manager_pod_role.id}"
  policy = "${file("cert-manager-role-rights.json")}"
}
