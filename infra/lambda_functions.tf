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
   LAMBDA FUNCTION: get-investment-portfolios
   Defines the AWS Lambda Function for getting data from
   an user's investment portfolio source
-------------------------------------------------------- */

module "aws_lambda_function_get_investment_portfolios" {
  source = "git::https://github.com/ThiagoPanini/tfbox.git?ref=aws/lambda-function/v0.6.0"

  function_name = "b3stocks-get-investment-portfolios"
  runtime       = "python3.12"
  timeout       = 180

  role_arn = module.aws_iam_roles.roles_arns["role-b3stocks-lambda-get-investment-portfolios"]

  source_code_path = "../app"
  lambda_handler   = "app.src.features.get_investment_portfolios.presentation.get_investment_portfolios_presentation.handler"

  environment_variables = {
    S3_ARTIFACTS_BUCKET_NAME_PREFIX          = var.s3_artifacts_bucket_name_prefix
    S3_INVESTMENT_PORTFOLIOS_KEY_PREFIX      = var.s3_investment_portfolios_key_prefix
    DYNAMODB_INVESTMENT_PORTFOLIO_TABLE_NAME = module.aws_dynamodb_table_tbl_b3stocks_investment_portfolio.table_name
  }

  layers_arns = [
    module.aws_lambda_layers.layers_arns["b3stocks-deps"]
  ]

  create_eventbridge_trigger = true
  cron_expression            = "cron(0 21 * * ? *)"

  tags = var.tags

  depends_on = [
    module.aws_iam_roles
  ]
}


/* --------------------------------------------------------
   LAMBDA FUNCTION: get-active-stocks
   Defines the AWS Lambda Function for getting active stocks
   data from a source website defined by user.
-------------------------------------------------------- */

module "aws_lambda_function_get_active_stocks" {
  source = "git::https://github.com/ThiagoPanini/tfbox.git?ref=aws/lambda-function/v0.6.0"

  function_name = "b3stocks-get-active-stocks"
  runtime       = "python3.12"
  timeout       = 180

  role_arn = module.aws_iam_roles.roles_arns["role-b3stocks-lambda-get-active-stocks"]

  source_code_path = "../app"
  lambda_handler   = "app.src.features.get_active_stocks.presentation.get_active_stocks_presentation.handler"

  environment_variables = {
    DYNAMODB_ACTIVE_STOCKS_TABLE_NAME = module.aws_dynamodb_table_tbl_b3stocks_active_stocks.table_name
  }

  layers_arns = [
    module.aws_lambda_layers.layers_arns["b3stocks-deps"]
  ]

  create_eventbridge_trigger = true
  cron_expression            = "cron(0 21 * * ? *)"

  tags = var.tags

  depends_on = [
    module.aws_iam_roles
  ]
}
