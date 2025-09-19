/* -----------------------------------------------------------------------------
  FILE: data.tf
  PROJECT: b3stocks

  DESCRIPTION:
    Centralized Terraform data source definitions for the b3stocks project.
    This file provides consistent access to AWS account information, region
    details, and AWS managed KMS keys, enabling dynamic and environment-aware
    resource provisioning throughout the infrastructure.

  DATA SOURCES:
    - aws_caller_identity.current: Retrieves the AWS account ID and user information
    - aws_region.current: Obtains the current AWS region in use
    - aws_kms_key.sns: Retrieves the AWS managed KMS key for SNS encryption
----------------------------------------------------------------------------- */

# Data sources for collecting AWS account information and region
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

# AWS managed KMS key for SNS encryption
data "aws_kms_key" "sns" {
  key_id = "alias/aws/sns"
}
