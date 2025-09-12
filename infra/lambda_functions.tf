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

module "aws_lambda_function_get_investment_portfolio" {
  source = "git::https://github.com/ThiagoPanini/tfbox.git?ref=aws/lambda-function/v0.5.0"

  function_name = "b3stocks-get-investment-portfolio"
  runtime       = "python3.12"
  timeout       = 180

  role_arn = module.aws_iam_roles.roles_arns["role-b3stocks-lambda-get-investment-portfolio"]

  source_code_path = "../app"
  lambda_handler   = "app.src.features.get_investment_portfolio.presentation.get_investment_portfolio_presentation.handler"

  environment_variables = {
    S3_ARTIFACTS_BUCKET_NAME_PREFIX          = var.s3_artifacts_bucket_name_prefix
    S3_INVESTMENT_PORTFOLIO_OBJECT_KEY       = var.s3_investment_portfolio_object_key
    DYNAMODB_INVESTMENT_PORTFOLIO_TABLE_NAME = module.aws_dynamodb_table_tbl_brstocks_investment_portfolio.table_name
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
   LAMBDA FUNCTION: stream-cdc-data (Generic CDC Writer)
   Processes CDC stream batches and lands JSON lines
   in S3 partitioned by event_date.
-------------------------------------------------------- */

module "aws_lambda_function_stream_cdc_data" {
  source = "git::https://github.com/ThiagoPanini/tfbox.git?ref=aws/lambda-function/v0.5.0"

  function_name = "b3stocks-stream-cdc-data"
  runtime       = var.lambda_function_common_runtime
  timeout       = 60

  role_arn = module.aws_iam_roles.roles_arns["role-b3stocks-lambda-stream-cdc-data"]

  source_code_path = "../app"
  # lambda_handler   = "app.src.features.cross.streaming.dynamodb_to_s3.handler.handler"
  lambda_handler = "app.src.features.stream_cdc_data.presentation.stream_cdc_data_presentation.handler"

  tags = var.tags

  depends_on = [
    module.aws_lambda_layers,
    module.aws_iam_roles
  ]
}

resource "aws_lambda_event_source_mapping" "dynamodb_stream_tbl_brstocks_investment_portfolio" {
  event_source_arn       = module.aws_dynamodb_table_tbl_brstocks_investment_portfolio.stream_arn
  function_name          = module.aws_lambda_function_stream_cdc_data.function_name
  starting_position      = "LATEST"
  batch_size             = 100
  maximum_retry_attempts = 2

  depends_on = [
    module.aws_lambda_function_stream_cdc_data,
    module.aws_dynamodb_table_tbl_brstocks_investment_portfolio
  ]
}

