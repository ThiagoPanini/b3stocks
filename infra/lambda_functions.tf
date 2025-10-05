/* -----------------------------------------------------------------------------
FILE: lambda_functions.tf
PROJECT: b3stocks

DESCRIPTION:
  This Terraform configuration defines AWS Lambda functions for the core
  b3stocks project features. Each function is configured with appropriate
  runtime environment, IAM roles, layers, and EventBridge triggers for
  scheduled execution.

FUNCTIONS:
  - b3stocks-get-investment-portfolios: Retrieves and processes user investment portfolios
  - b3stocks-get-active-stocks: Collects active stock data from B3 sources
  - b3stocks-get-fundamentus-eod-stock-metrics: Fetches end-of-day stock metrics from Fundamentus
----------------------------------------------------------------------------- */

/* --------------------------------------------------------
   LAMBDA FUNCTION: get-investment-portfolios
   Retrieves investment portfolio data from S3, processes
   it, and stores the results in DynamoDB. Scheduled to
   run daily at 21:00 UTC via EventBridge.
-------------------------------------------------------- */

/*
module "aws_lambda_function_get_investment_portfolios" {
  source = "git::https://github.com/ThiagoPanini/tfbox.git?ref=aws/lambda-function/v0.7.0"

  function_name = "b3stocks-get-investment-portfolios"
  description = "Retrieves investment portfolio data from S3 and stores it in DynamoDB"
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
*/

/* --------------------------------------------------------
   LAMBDA FUNCTION: get-active-stocks
   Scrapes active stock data from B3 sources, processes
   the information, and stores it in DynamoDB. Publishes
   notifications to SNS. Scheduled daily at 21:00 UTC.
-------------------------------------------------------- */

module "aws_lambda_function_get_active_stocks" {
  source = "git::https://github.com/ThiagoPanini/tfbox.git?ref=aws/lambda-function/v0.7.0"

  function_name = "b3stocks-get-active-stocks"
  description   = "Scrapes active stock data from an investment website"
  runtime       = "python3.12"
  timeout       = 180

  role_arn = module.aws_iam_roles.roles_arns["role-b3stocks-lambda-get-active-stocks"]

  source_code_path = "../app"
  lambda_handler   = "app.src.features.get_active_stocks.presentation.get_active_stocks_presentation.handler"

  environment_variables = {
    DYNAMODB_ACTIVE_STOCKS_TABLE_NAME = module.aws_dynamodb_table_tbl_b3stocks_active_stocks.table_name
    SNS_ACTIVE_STOCKS_TOPIC_NAME      = module.sns_topic_active_stocks.topic_name
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
   LAMBDA FUNCTION: get-fundamentus-eod-stock-metrics
   Fetches end-of-day stock metrics from Fundamentus website,
   processes financial data, and stores it in S3. Triggered
   by SQS messages from active stocks SNS topic.
-------------------------------------------------------- */

module "aws_lambda_function_get_fundamentus_eod_stock_metrics" {
  source = "git::https://github.com/ThiagoPanini/tfbox.git?ref=aws/lambda-function/v0.7.0"

  function_name = "b3stocks-get-fundamentus-eod-stock-metrics"
  description   = "Fetches end-of-day different stock metrics from Fundamentus website"
  runtime       = "python3.12"
  timeout       = 180

  role_arn = module.aws_iam_roles.roles_arns["role-b3stocks-lambda-get-fundamentus-eod-stock-metrics"]

  source_code_path = "../app"
  lambda_handler   = "app.src.features.get_fundamentus_eod_stock_metrics.presentation.get_fundamentus_eod_stock_metrics_presentation.handler"

  environment_variables = {
    DYNAMODB_FUNDAMENTUS_EOD_STOCK_METRICS_TABLE_NAME = module.aws_dynamodb_table_tbl_b3stocks_fundamentus_eod_stock_metrics.table_name
    DYNAMODB_BATCH_PROCESS_CONTROL_TABLE_NAME         = module.aws_dynamodb_table_tbl_b3stocks_batch_process_control.table_name
  }

  layers_arns = [
    module.aws_lambda_layers.layers_arns["b3stocks-deps"],
    "arn:aws:lambda:${local.region_name}:336392948345:layer:AWSSDKPandas-Python312:18"
  ]

  tags = var.tags

  depends_on = [
    module.aws_iam_roles
  ]
}

# Trigger the Lambda from SQS Queue
resource "aws_lambda_event_source_mapping" "queue-fundamentus-eod-stock-metrics" {
  function_name    = module.aws_lambda_function_get_fundamentus_eod_stock_metrics.function_name
  event_source_arn = module.sqs_queue_fundamentus_eod_stock_metrics.queue_arn

  batch_size                         = 100
  maximum_batching_window_in_seconds = 10

  scaling_config {
    maximum_concurrency = 3
  }

  depends_on = [
    module.aws_lambda_function_get_fundamentus_eod_stock_metrics,
    module.sqs_queue_fundamentus_eod_stock_metrics
  ]
}


/* --------------------------------------------------------
   LAMBDA FUNCTION: check-batch-processes-completion
   Checks the completion status of the batch processes
   in the batch process control table
-------------------------------------------------------- */

module "aws_lambda_function_check_batch_processes_completion" {
  source = "git::https://github.com/ThiagoPanini/tfbox.git?ref=aws/lambda-function/v0.7.0"

  function_name = "b3stocks-check-batch-processes-completion"
  description   = "Checks the completion status of the batch processes"
  runtime       = "python3.12"
  timeout       = 180

  role_arn = module.aws_iam_roles.roles_arns["role-b3stocks-lambda-check-batch-processes-completion"]

  source_code_path = "../app"
  lambda_handler   = "app.src.features.check_batch_processes_completion.presentation.check_batch_processes_completion_presentation.handler"

  layers_arns = [
    module.aws_lambda_layers.layers_arns["b3stocks-deps"]
  ]

  tags = var.tags

  depends_on = [
    module.aws_iam_roles
  ]
}

# Trigger Lambda from DynamoDB Streams
resource "aws_lambda_event_source_mapping" "dynamodb_stream_check_batch_processes_completion" {
  event_source_arn       = module.aws_dynamodb_table_tbl_b3stocks_batch_process_control.stream_arn
  function_name          = module.aws_lambda_function_check_batch_processes_completion.function_name
  starting_position      = "LATEST"
  batch_size             = 5
  maximum_retry_attempts = 1

  depends_on = [
    module.aws_lambda_function_check_batch_processes_completion,
    module.aws_dynamodb_table_tbl_b3stocks_batch_process_control
  ]
}


/* --------------------------------------------------------
   LAMBDA FUNCTION: send-batch-completion-emails
   Receives notification from SNS topic and sends emails
   about batch processes completion using SES.
-------------------------------------------------------- */

module "aws_lambda_function_send_batch_completion_emails" {
  source = "git::https://github.com/ThiagoPanini/tfbox.git?ref=aws/lambda-function/v0.7.0"

  function_name = "b3stocks-send-batch-completion-emails"
  description   = "Sends emails about batch processes completion"
  runtime       = "python3.12"
  timeout       = 180

  role_arn = module.aws_iam_roles.roles_arns["role-b3stocks-lambda-send-batch-completion-emails"]

  source_code_path = "../app"
  lambda_handler   = "app.src.features.send_batch_completion_emails.presentation.send_batch_completion_emails_presentation.handler"

  tags = var.tags

  depends_on = [
    module.aws_iam_roles
  ]
}

# Allow SNS to invoke the Lambda function
resource "aws_lambda_permission" "allow_sns_batch_completion" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = module.aws_lambda_function_send_batch_completion_emails.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = module.sns_topic_batch_processes_completion.topic_arn

  depends_on = [
    module.aws_lambda_function_send_batch_completion_emails,
    module.sns_topic_batch_processes_completion
  ]
}
