/* -----------------------------------------------------------------------------
  FILE: role.tf
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


module "iam_role_lambda" {
  source = "git::https://github.com/ThiagoPanini/tfbox.git?ref=aws/iam-role/v0.2.0"

  role_name                   = "techplay-get-b3-stock-tickers-lambda-role"
  trust_policy_filepath       = "${path.module}/assets/iam/trust_policies/trust-lambda.json"
  policy_templates_source_dir = "${path.module}/assets/iam/policy_templates"

  policy_templates_vars = {
    "region_name"  = local.region_name,
    "account_id"   = local.account_id,
    "topic_name"   = var.sns_topic_name,
    "bucket_name"  = local.bucket_name
    "table_prefix" = var.glue_table_name
  }
}
