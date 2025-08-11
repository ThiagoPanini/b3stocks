/* -----------------------------------------------------------------------------
FILE: lambda.tf @ get-b3-active-tickers module

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

module "lambda_function" {
  source = "git::https://github.com/ThiagoPanini/tfbox.git?ref=aws/lambda-function/v0.3.1"

  function_name = var.lambda_function_name
  runtime       = var.lambda_function_runtime
  architectures = var.lambda_function_architectures
  timeout       = var.lambda_function_timeout_seconds

  role_arn = module.iam_role_lambda.role_arn

  source_code_path = "../../../app"
  lambda_handler   = "app.src.features.get_b3_stock_tickers.presentation.get_b3_stock_tickers_presentation.handler"

  environment_variables = {
    DYNAMODB_B3_STOCK_TICKERS_TABLE_NAME = var.dynamodb_table_name
    SNS_B3_STOCK_TICKERS_TOPIC_NAME      = var.sns_topic_name
  }

  create_lambda_layers = true
  layers_map = {
    techplay_b3_tickers_layer = {
      requirements = [
        "beautifulsoup4==4.13.3",
        "boto3==1.36.23",
        "pydantic==2.10.6",
        "requests==2.32.3",
      ]
      runtime     = "python3.12"
      description = "Dependencies for getting b3 stock tickers from financial web sites"
    }
  }

  create_eventbridge_trigger = true
  cron_expression            = var.lambda_function_cron_expression

  tags = var.tags
}
