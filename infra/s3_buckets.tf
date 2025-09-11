/* -----------------------------------------------------------------------------
  FILE: s3.tf

  DESCRIPTION:
    This Terraform file provisions all S3 buckets required by all app features
    on b3stocks project.

  RESOURCES:
    - aws_s3_bucket.artifacts:
        Creates an S3 bucket for storing artifacts on b3stocks project

    - aws_s3_bucket_public_access_block.artifacts_bucket_public_access_block:
        Blocks all public access to the artifacts S3 bucket.
----------------------------------------------------------------------------- */

/* --------------------------------------------------------
   S3 BUCKET: Artifacts
   A S3 bucket for storing artifacts on b3stocks project.
-------------------------------------------------------- */

resource "aws_s3_bucket" "artifacts" {
  bucket = local.s3_artifacts_bucket_name
  tags   = var.tags
}

resource "aws_s3_bucket_public_access_block" "artifacts_bucket_public_access_block" {
  bucket                  = aws_s3_bucket.artifacts.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true

  depends_on = [
    aws_s3_bucket.artifacts
  ]
}

/* --------------------------------------------------------
   S3 BUCKET: Analytics Bronze
   Stores bronze data got by any source.
-------------------------------------------------------- */

resource "aws_s3_bucket" "analytics_bronze" {
  bucket = local.s3_analytics_bronze_bucket_name
  tags   = var.tags
}

resource "aws_s3_bucket_public_access_block" "analytics_bronze_public_access_block" {
  bucket                  = aws_s3_bucket.analytics_bronze.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true

  depends_on = [
    aws_s3_bucket.analytics_bronze
  ]
}
