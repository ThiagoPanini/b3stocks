/* -----------------------------------------------------------------------------
  FILE: s3_buckets.tf
  PROJECT: b3stocks

  DESCRIPTION:
    This Terraform file provisions all S3 buckets required by the b3stocks
    project. Each bucket is configured with appropriate access controls and
    serves specific purposes in the data pipeline architecture.

  BUCKETS:
    - artifacts: Stores application artifacts including investment portfolio files
    - analytics_cdc: Stores Change Data Capture data from DynamoDB streams
    - analytics_sor: Stores System of Record data in Parquet format for analytics
----------------------------------------------------------------------------- */

/* --------------------------------------------------------
   S3 BUCKET: Artifacts
   Stores application artifacts including investment portfolio
   YAML files and other configuration data. Configured with
   force_destroy for development environments.
-------------------------------------------------------- */

resource "aws_s3_bucket" "artifacts" {
  bucket        = local.s3_artifacts_bucket_name
  force_destroy = true
  tags          = var.tags
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
   S3 BUCKET: Analytics CDC
   Stores Change Data Capture data streamed from DynamoDB
   tables. Contains JSON records of data changes partitioned
   by event date for efficient analytics processing.
-------------------------------------------------------- */

resource "aws_s3_bucket" "analytics_cdc" {
  bucket        = local.s3_analytics_cdc_bucket_name
  force_destroy = true
  tags          = var.tags
}

resource "aws_s3_bucket_public_access_block" "analytics_cdc_public_access_block" {
  bucket                  = aws_s3_bucket.analytics_cdc.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true

  depends_on = [
    aws_s3_bucket.analytics_cdc
  ]
}


/* --------------------------------------------------------
   S3 BUCKET: Analytics SoR
   Stores System of Record data in Parquet format for
   analytics workloads. Contains processed and cleaned
   data optimized for query performance.
-------------------------------------------------------- */

resource "aws_s3_bucket" "analytics_sor" {
  bucket        = local.s3_analytics_sor_bucket_name
  force_destroy = true
  tags          = var.tags
}

resource "aws_s3_bucket_public_access_block" "analytics_sor_bucket_public_access_block" {
  bucket                  = aws_s3_bucket.analytics_sor.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true

  depends_on = [
    aws_s3_bucket.analytics_sor
  ]
}
