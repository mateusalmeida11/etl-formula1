terraform {
  backend "s3" {
    bucket       = "mateusalmeida-us-east-1-terraform-statefile-with-lock"
    key          = "dev/statefile.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true
  }
}
