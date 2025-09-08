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

resource "aws_s3_object" "investment_portfolio_csv" {
  bucket = aws_s3_bucket.artifacts.id
  key    = var.s3_investment_portfolio_object_key
  source = "${path.module}/assets/investment_portfolio/b3_investment_portfolio.csv"
  etag   = filemd5("${path.module}/assets/investment_portfolio/b3_investment_portfolio.csv")

  content_type = "text/csv"

  tags = var.tags

  depends_on = [
    aws_s3_bucket.artifacts,
    aws_s3_bucket_public_access_block.artifacts_bucket_public_access_block
  ]

}
