terraform {
  backend "s3" {
    bucket = "cs4300-terraform-state"
    key    = "certmanager/terraform.tfstate"
    region = "us-east-1"
  }
}
