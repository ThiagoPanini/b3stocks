/* -----------------------------------------------------------------------------
FILE: iam.tf

DESCRIPTION:
  This Terraform file centralizes the IAM Role definitions for all applications
  and services used in the b3stocks project.

RESOURCES:
  - module.iam_roles:
    Deplpoys IAM roles using the tfbox module with configurable properties such as
    role names, trust policies, and attached policies.
----------------------------------------------------------------------------- */

module "aws_iam_roles" {
  source = "git::https://github.com/ThiagoPanini/tfbox.git?ref=aws/iam-role/v0.3.0"

  policies_template_config = {
    templates_source_dir = "${path.module}/assets/iam/policy_templates"
    templates_vars = {
      "region_name"                              = local.region_name,
      "account_id"                               = local.account_id,
      "s3_artifacts_bucket_name"                 = local.s3_artifacts_bucket_name,
      "s3_investment_portfolio_object_key"       = var.s3_investment_portfolio_object_key
      "dynamodb_investment_portfolio_table_name" = module.aws_dynamodb_table_tbl_brstocks_investment_portfolio.table_name
      "s3_analytics_cdc_bucket_name"             = local.s3_analytics_cdc_bucket_name
    }
  }

  roles_config = [
    {
      role_name             = "role-b3stocks-lambda-get-investment-portfolio"
      trust_policy_filepath = "${path.module}/assets/iam/trust_policies/trust-lambda.json"
      policies_arns = [
        "arn:aws:iam::${local.account_id}:policy/policy-b3stocks-lambda-cloudwatch-logs",
        "arn:aws:iam::${local.account_id}:policy/policy-b3stocks-get-investment-portfolio",
      ]
    },
    {
      role_name             = "role-b3stocks-lambda-stream-cdc-data"
      trust_policy_filepath = "${path.module}/assets/iam/trust_policies/trust-lambda.json"
      policies_arns = [
        "arn:aws:iam::${local.account_id}:policy/policy-b3stocks-lambda-cloudwatch-logs",
        "arn:aws:iam::${local.account_id}:policy/policy-b3stocks-stream-cdc-data",
      ]
    }
  ]
}
