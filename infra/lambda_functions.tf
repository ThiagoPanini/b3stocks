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
   LAMBDA FUNCTION: stream-investment-portfolios
   Processes CDC stream batches and lands JSON lines
   in S3 partitioned by event_date for lambda function
   get-investment-portfolio
-------------------------------------------------------- */

module "aws_lambda_function_stream_investment_portfolios" {
  source = "git::https://github.com/ThiagoPanini/tfbox.git?ref=aws/lambda-function/v0.6.0"

  function_name = "b3stocks-stream-investment-portfolios"
  runtime       = var.lambda_function_common_runtime
  timeout       = 60

  role_arn = module.aws_iam_roles.roles_arns["role-b3stocks-lambda-stream-investment-portfolios"]

  source_code_path = "../app"
  lambda_handler   = "app.src.features.store_dynamodb_streams_data.presentation.store_dynamodb_streams_data_presentation.handler"

  environment_variables = {
    S3_ANALYTICS_CDC_BUCKET_NAME_PREFIX = var.s3_analytics_cdc_bucket_name_prefix
    S3_ANALYTICS_SOR_BUCKET_NAME_PREFIX = var.s3_analytics_sor_bucket_name_prefix
    DATA_CATALOG_CDC_DATABASE_NAME      = aws_glue_catalog_database.b3stocks_analytics_cdc.name
    DATA_CATALOG_SOR_DATABASE_NAME      = aws_glue_catalog_database.b3stocks_analytics_sor.name
  }

  layers_arns = [
    "arn:aws:lambda:${local.region_name}:336392948345:layer:AWSSDKPandas-Python312:18"
  ]

  tags = var.tags

  depends_on = [
    module.aws_lambda_layers,
    module.aws_iam_roles
  ]
}

resource "aws_lambda_event_source_mapping" "dynamodb_stream_tbl_b3stocks_investment_portfolios" {
  event_source_arn       = module.aws_dynamodb_table_tbl_b3stocks_investment_portfolio.stream_arn
  function_name          = module.aws_lambda_function_stream_investment_portfolios.function_name
  starting_position      = "LATEST"
  batch_size             = 100
  maximum_retry_attempts = 1

  depends_on = [
    module.aws_lambda_function_stream_investment_portfolios,
    module.aws_dynamodb_table_tbl_b3stocks_investment_portfolio
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


/* --------------------------------------------------------
   LAMBDA FUNCTION: stream-active-stocks
   Processes CDC stream batches and lands JSON lines
   in S3 partitioned by event_date for lambda function
   get-active-stocks
-------------------------------------------------------- */

module "aws_lambda_function_stream_active_stocks" {
  source = "git::https://github.com/ThiagoPanini/tfbox.git?ref=aws/lambda-function/v0.6.0"

  function_name = "b3stocks-stream-active-stocks"
  runtime       = var.lambda_function_common_runtime
  timeout       = 300

  role_arn = module.aws_iam_roles.roles_arns["role-b3stocks-lambda-stream-active-stocks"]

  source_code_path = "../app"
  lambda_handler   = "app.src.features.store_dynamodb_streams_data.presentation.store_dynamodb_streams_data_presentation.handler"

  environment_variables = {
    S3_ANALYTICS_CDC_BUCKET_NAME_PREFIX = var.s3_analytics_cdc_bucket_name_prefix
    S3_ANALYTICS_SOR_BUCKET_NAME_PREFIX = var.s3_analytics_sor_bucket_name_prefix
    DATA_CATALOG_CDC_DATABASE_NAME      = aws_glue_catalog_database.b3stocks_analytics_cdc.name
    DATA_CATALOG_SOR_DATABASE_NAME      = aws_glue_catalog_database.b3stocks_analytics_sor.name
  }

  layers_arns = [
    "arn:aws:lambda:${local.region_name}:336392948345:layer:AWSSDKPandas-Python312:18"
  ]

  tags = var.tags

  depends_on = [
    module.aws_lambda_layers,
    module.aws_iam_roles
  ]
}

resource "aws_lambda_event_source_mapping" "dynamodb_stream_tbl_b3stocks_active_stocks" {
  event_source_arn       = module.aws_dynamodb_table_tbl_b3stocks_active_stocks.stream_arn
  function_name          = module.aws_lambda_function_stream_active_stocks.function_name
  starting_position      = "LATEST"
  batch_size             = 100
  maximum_retry_attempts = 1

  depends_on = [
    module.aws_lambda_function_stream_active_stocks,
    module.aws_dynamodb_table_tbl_b3stocks_active_stocks
  ]
}
