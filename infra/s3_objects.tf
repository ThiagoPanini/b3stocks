/* -----------------------------------------------------------------------------
  FILE: s3_objects.tf

  DESCRIPTION:
    This Terraform file provisions all S3 objects required by all app features
    on b3stocks project.

  RESOURCES:
    - aws_s3_bucket.artifacts:
        Creates an S3 bucket for storing artifacts on b3stocks project

    - aws_s3_bucket_public_access_block.artifacts_bucket_public_access_block:
        Blocks all public access to the artifacts S3 bucket.
----------------------------------------------------------------------------- */


/* --------------------------------------------------------
   S3 OBJECT(S): B3 Investment Portfolio
   Uploads a CSV file containing B3 investment portfolio
   data to the artifacts S3 bucket.
-------------------------------------------------------- */

# Uploading all local portfolio files to S3
resource "aws_s3_object" "investment_portfolios" {
  for_each = toset(local.portfolios_files)
  bucket   = aws_s3_bucket.artifacts.id
  key      = "investment_portfolios/${each.value}"
  source   = "${path.module}/assets/investment_portfolios/${each.value}"
  etag     = filemd5("${path.module}/assets/investment_portfolios/${each.value}")

  content_type = "application/yaml"

  tags = var.tags

  depends_on = [
    aws_s3_bucket.artifacts,
    aws_s3_bucket_public_access_block.artifacts_bucket_public_access_block
  ]

}
