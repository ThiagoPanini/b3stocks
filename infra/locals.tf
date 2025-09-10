/* -----------------------------------------------------------------------------
  FILE: locals.tf
  MODULE: aws/get_b3_stock_tickers

  DESCRIPTION:
    This file defines local variables for the aws/get_b3_stock_tickers Terraform
    module. The purpose of these locals is to centralize dynamic values—such as
    the AWS account ID and region name—retrieved at runtime.

  LOCAL VARIABLES:
    - account_id: The AWS account ID of the current caller.
    - region_name: The AWS region in which resources are being deployed.
----------------------------------------------------------------------------- */


locals {
  # Extracting account ID and region name
  account_id  = data.aws_caller_identity.current.account_id
  region_name = data.aws_region.current.name

  # Bucket names
  s3_artifacts_bucket_name        = "b3stocks-artifacts-${local.account_id}-${local.region_name}"
  s3_analytics_bronze_bucket_name = "b3stocks-analytics-bronze-${local.account_id}-${local.region_name}"
}
