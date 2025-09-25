/* -----------------------------------------------------------------------------
  FILE: versions.tf
  PROJECT: b3stocks

  DESCRIPTION:
    Terraform and provider version constraints for the b3stocks infrastructure.
    This file ensures consistent deployments by specifying minimum required
    versions and compatible version ranges for Terraform and AWS provider.

  REQUIREMENTS:
    - Terraform: >= 1.9
    - AWS Provider: ~> 5.50 (compatible with 5.50.x)
----------------------------------------------------------------------------- */


terraform {
  required_version = ">= 1.9"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.50"
    }
  }
}
