/* -----------------------------------------------------------------------------
FILE: iam_roles.tf
PROJECT: b3stocks

DESCRIPTION:
  This Terraform file centralizes all IAM role definitions and policy
  configurations for the b3stocks project. It creates roles with appropriate
  trust policies and permissions for Lambda functions to access AWS services
  including DynamoDB, S3, SNS, SQS, and CloudWatch.

ROLES:
  - role-b3stocks-lambda-get-active-stocks: Lambda role for stock data collection
  - role-b3stocks-lambda-get-fundamentus-eod-stock-metrics: Lambda role for metrics collection
  - role-b3stocks-lambda-stream-active-stocks: Lambda role for stocks CDC processing
  - role-b3stocks-lambda-stream-fundamentus-eod-stock-metrics: Lambda role for metrics CDC processing
  - role-b3stocks-lambda-stream-batch-process-control: Lambda role for batch process control CDC
  - role-b3stocks-lambda-check-batch-processes-completion: Lambda role for checking batch process completion
----------------------------------------------------------------------------- */

module "aws_iam_roles" {
  source = "git::https://github.com/ThiagoPanini/tfbox.git?ref=aws/iam-role/v0.3.0"

  policies_template_config = {
    templates_source_dir = "${path.module}/assets/iam/policy_templates"
    templates_vars = {
      "region_name"                                       = local.region_name
      "account_id"                                        = local.account_id
      "s3_artifacts_bucket_name"                          = local.s3_artifacts_bucket_name
      "s3_analytics_cdc_bucket_name"                      = local.s3_analytics_cdc_bucket_name
      "s3_analytics_sor_bucket_name"                      = local.s3_analytics_sor_bucket_name
      "s3_investment_portfolios_key_prefix"               = var.s3_investment_portfolios_key_prefix
      "s3_email_templates_folder_prefix"                  = var.s3_email_templates_folder_prefix
      "dynamodb_investment_portfolio_table_name"          = module.aws_dynamodb_table_tbl_b3stocks_investment_portfolio.table_name
      "dynamodb_active_stocks_table_name"                 = module.aws_dynamodb_table_tbl_b3stocks_active_stocks.table_name
      "dynamodb_fundamentus_eod_stock_metrics_table_name" = module.aws_dynamodb_table_tbl_b3stocks_fundamentus_eod_stock_metrics.table_name
      "dynamodb_batch_process_control_table_name"         = module.aws_dynamodb_table_tbl_b3stocks_batch_process_control.table_name
      "sns_active_stocks_topic_name"                      = module.sns_topic_active_stocks.topic_name
      "sns_batch_processes_completion_topic_name"         = module.sns_topic_batch_processes_completion.topic_name
      "sqs_fundamentus_eod_stock_metrics_queue_name"      = module.sqs_queue_fundamentus_eod_stock_metrics.queue_name
      "data_catalog_cdc_database_name"                    = aws_glue_catalog_database.b3stocks_analytics_cdc.name
      "data_catalog_sor_database_name"                    = aws_glue_catalog_database.b3stocks_analytics_sor.name
    }
  }

  roles_config = [
    /*
    {
      role_name             = "role-b3stocks-lambda-get-investment-portfolios"
      trust_policy_filepath = "${path.module}/assets/iam/trust_policies/trust-lambda.json"
      policies_arns = [
        "arn:aws:iam::${local.account_id}:policy/policy-b3stocks-lambda-cloudwatch-logs",
        "arn:aws:iam::${local.account_id}:policy/policy-b3stocks-get-investment-portfolios",
      ]
    },
    */
    {
      role_name             = "role-b3stocks-lambda-get-active-stocks"
      trust_policy_filepath = "${path.module}/assets/iam/trust_policies/trust-lambda.json"
      policies_arns = [
        "arn:aws:iam::${local.account_id}:policy/policy-b3stocks-lambda-cloudwatch-logs",
        "arn:aws:iam::${local.account_id}:policy/policy-b3stocks-get-active-stocks",
      ]
    },
    {
      role_name             = "role-b3stocks-lambda-stream-active-stocks"
      trust_policy_filepath = "${path.module}/assets/iam/trust_policies/trust-lambda.json"
      policies_arns = [
        "arn:aws:iam::${local.account_id}:policy/policy-b3stocks-lambda-cloudwatch-logs",
        "arn:aws:iam::${local.account_id}:policy/policy-b3stocks-stream-active-stocks",
      ]
    },
    {
      role_name             = "role-b3stocks-lambda-get-fundamentus-eod-stock-metrics"
      trust_policy_filepath = "${path.module}/assets/iam/trust_policies/trust-lambda.json"
      policies_arns = [
        "arn:aws:iam::${local.account_id}:policy/policy-b3stocks-lambda-cloudwatch-logs",
        "arn:aws:iam::${local.account_id}:policy/policy-b3stocks-get-fundamentus-eod-stock-metrics",
      ]
    },
    {
      role_name             = "role-b3stocks-lambda-stream-fundamentus-eod-stock-metrics"
      trust_policy_filepath = "${path.module}/assets/iam/trust_policies/trust-lambda.json"
      policies_arns = [
        "arn:aws:iam::${local.account_id}:policy/policy-b3stocks-lambda-cloudwatch-logs",
        "arn:aws:iam::${local.account_id}:policy/policy-b3stocks-stream-fundamentus-eod-stock-metrics",
      ]
    },
    /*
    {
      role_name             = "role-b3stocks-lambda-stream-investment-portfolios"
      trust_policy_filepath = "${path.module}/assets/iam/trust_policies/trust-lambda.json"
      policies_arns = [
        "arn:aws:iam::${local.account_id}:policy/policy-b3stocks-lambda-cloudwatch-logs",
        "arn:aws:iam::${local.account_id}:policy/policy-b3stocks-stream-investment-portfolios",
      ]
    },
    */
    {
      role_name             = "role-b3stocks-lambda-stream-batch-process-control"
      trust_policy_filepath = "${path.module}/assets/iam/trust_policies/trust-lambda.json"
      policies_arns = [
        "arn:aws:iam::${local.account_id}:policy/policy-b3stocks-lambda-cloudwatch-logs",
        "arn:aws:iam::${local.account_id}:policy/policy-b3stocks-stream-batch-process-control",
      ]
    },
    {
      role_name             = "role-b3stocks-lambda-check-batch-processes-completion"
      trust_policy_filepath = "${path.module}/assets/iam/trust_policies/trust-lambda.json"
      policies_arns = [
        "arn:aws:iam::${local.account_id}:policy/policy-b3stocks-lambda-cloudwatch-logs",
        "arn:aws:iam::${local.account_id}:policy/policy-b3stocks-check-batch-processes-completion",
      ]
    },
    {
      role_name             = "role-b3stocks-lambda-send-batch-processes-completion-mails"
      trust_policy_filepath = "${path.module}/assets/iam/trust_policies/trust-lambda.json"
      policies_arns = [
        "arn:aws:iam::${local.account_id}:policy/policy-b3stocks-lambda-cloudwatch-logs",
        "arn:aws:iam::${local.account_id}:policy/policy-b3stocks-send-batch-processes-completion-mails",
      ]
    }
  ]
}
