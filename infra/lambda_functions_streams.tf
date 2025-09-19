/* -----------------------------------------------------------------------------
FILE: lambda_functions_streams.tf
PROJECT: b3stocks

DESCRIPTION:
  This Terraform configuration defines AWS Lambda functions for processing
  DynamoDB Streams data in the b3stocks project. These functions handle
  Change Data Capture (CDC) events from DynamoDB tables and store them
  in S3 for analytics purposes.

FUNCTIONS:
  - b3stocks-stream-investment-portfolios: Processes investment portfolio CDC events
  - b3stocks-stream-active-stocks: Processes active stocks CDC events

EVENT SOURCE MAPPINGS:
  - DynamoDB Stream triggers for real-time CDC processing
----------------------------------------------------------------------------- */


/* --------------------------------------------------------
   LAMBDA FUNCTION: stream-investment-portfolios
   Processes Change Data Capture events from investment
   portfolio DynamoDB table and stores JSON records in S3
   partitioned by event_date for analytics processing.
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
   LAMBDA FUNCTION: stream-active-stocks
   Processes Change Data Capture events from active stocks
   DynamoDB table and stores JSON records in S3 partitioned
   by event_date for analytics processing.
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
