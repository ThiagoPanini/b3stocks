/* -----------------------------------------------------------------------------
  FILE: locals.tf
  PROJECT: b3stocks

  DESCRIPTION:
    This file defines local variables for the b3stocks Terraform infrastructure.
    These locals centralize dynamic values retrieved at runtime and construct
    resource names following consistent naming conventions across the project.

  LOCAL VARIABLES:
    - account_id: AWS account ID from current caller identity
    - region_name: AWS region name where resources are deployed
    - s3_*_bucket_name: Constructed S3 bucket names with account and region suffixes
    - portfolios_files: List of portfolio YAML files for S3 upload
----------------------------------------------------------------------------- */


locals {
  # Extracting AWS account ID and region name from data sources
  account_id  = data.aws_caller_identity.current.account_id
  region_name = data.aws_region.current.name

  # Constructing S3 bucket names with account and region for global uniqueness
  s3_artifacts_bucket_name     = "${var.s3_artifacts_bucket_name_prefix}-${local.account_id}-${local.region_name}"
  s3_analytics_cdc_bucket_name = "${var.s3_analytics_cdc_bucket_name_prefix}-${local.account_id}-${local.region_name}"
  s3_analytics_sor_bucket_name = "${var.s3_analytics_sor_bucket_name_prefix}-${local.account_id}-${local.region_name}"

  # Investment portfolio files from local assets for S3 upload
  portfolios_files = fileset("${path.module}/assets/investment_portfolios", "*.yaml")

  # Email template files from local assets for S3 upload
  email_template_files = fileset("${path.module}/assets/email_templates", "*.html")
}
