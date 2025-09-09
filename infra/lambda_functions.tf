/* -----------------------------------------------------------------------------
FILE: lambda.tf

DESCRIPTION:
  This Terraform configuration uses a remote module to provision an AWS Lambda
  function for processing B3 active tickers. The function's name, runtime,
  handler, and environment variables are parameterized via input variables for
  flexible deployments.

RESOURCES:
  - module.aws_lambda_function:
    Deploys a Lambda function using the tfbox module with configurable properties
    such as name, runtime, handler, and environment variables.
----------------------------------------------------------------------------- */

/* --------------------------------------------------------
   LAMBDA FUNCTION: get-investment-portfolio
   Defines the AWS Lambda Function for getting data from
   an user's investment portfolio source
-------------------------------------------------------- */

module "iam_role_lambda_get_investment_portfolio" {
  source = "git::https://github.com/ThiagoPanini/tfbox.git?ref=aws/iam-role/v0.2.0"

  role_name                   = "role-b3stocks-get-investment-portfolio"
  trust_policy_filepath       = "${path.module}/assets/iam/trust_policies/trust-lambda.json"
  policy_templates_source_dir = "${path.module}/assets/iam/policy_templates"

  policy_templates_vars = {
    "region_name" = local.region_name,
    "account_id"  = local.account_id,
    "bucket_name" = local.s3_artifacts_bucket_name,
    "object_key"  = var.s3_investment_portfolio_object_key
  }
}

module "lambda_function_get_investment_portfolio" {
  source = "git::https://github.com/ThiagoPanini/tfbox.git?ref=aws/lambda-function/v0.4.0"

  function_name = "b3stocks-get-investment-portfolio"
  runtime       = "python3.12"
  timeout       = 180

  role_arn = module.iam_role_lambda_get_investment_portfolio.role_arn

  source_code_path = "../app"
  lambda_handler   = "app.src.features.get_investment_portfolio.presentation.get_investment_portfolio_presentation.handler"

  environment_variables = {
    S3_ARTIFACT_BUCKET_NAME            = local.s3_artifacts_bucket_name
    S3_INVESTMENT_PORTFOLIO_OBJECT_KEY = var.s3_investment_portfolio_object_key
  }

  managed_layers_arns = module.aws_lambda_layers.layers_arns

  create_eventbridge_trigger = true
  cron_expression            = "cron(0 21 * * ? *)"

  tags = var.tags
}
