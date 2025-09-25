/* -----------------------------------------------------------------------------
  FILE: s3_objects.tf
  PROJECT: b3stocks

  DESCRIPTION:
    This Terraform file uploads required objects to S3 buckets for the
    b3stocks project. These objects include configuration files and
    reference data used by Lambda functions during processing.

  OBJECTS:
    - investment_portfolios/*.yaml: User investment portfolio configuration files
----------------------------------------------------------------------------- */


/* --------------------------------------------------------
   S3 OBJECT(S): Investment Portfolio Files
   Uploads all YAML investment portfolio configuration files
   from local assets directory to S3 artifacts bucket.
   Files are used by Lambda functions to process user portfolios.
-------------------------------------------------------- */

# Upload all portfolio YAML files to S3 with proper content type
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
