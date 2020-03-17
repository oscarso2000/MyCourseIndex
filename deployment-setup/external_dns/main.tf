terraform {
  backend "s3" {
    bucket = "cs4300-terraform-state"
    key    = "externaldns/terraform.tfstate"
    region = "us-east-1"
  }
}