/* -----------------------------------------------------------------------------
  FILE: s3.tf
  MODULE: aws/get-b3-stock-tickers

  DESCRIPTION:
    This Terraform file uses a module to provision an AWS IAM role for the
    "get-b3-stock-tickers" Lambda function. The role's trust policy is loaded
    from an external JSON file, and inline policies are generated from templates
    with variable substitution.

  RESOURCES:
    - module.aws_iam_role:
        Provisions an IAM role with a trust policy and attaches inline policies
        generated from templates. The module supports variable substitution for
        policy templates and uses external files for trust policy configuration.
----------------------------------------------------------------------------- */

resource "aws_s3_bucket" "private_bucket" {
  bucket = local.bucket_name

  tags = var.tags
}

resource "aws_s3_bucket_public_access_block" "private_bucket_block" {
  bucket                  = aws_s3_bucket.private_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
