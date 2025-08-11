/* -----------------------------------------------------------------------------
  FILE: data.tf
  MODULE: aws/get-b3-stock-tickers

  DESCRIPTION:
    Centralized Terraform data source definitions for the AWS get-b3-stock-tickers
    module. This file provides consistent access to AWS account and region
    information, enabling dynamic and environment-aware resource provisioning
    throughout the module.

  DATA SOURCES:
    - aws_caller_identity.current: Retrieves the AWS account ID and user information.
    - aws_region.current: Obtains the current AWS region in use.
----------------------------------------------------------------------------- */

# Defining data sources for collecting account ID and region name
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

# Colleting AWS managed key for SNS
data "aws_kms_key" "sns" {
  key_id = "alias/aws/sns"
}
