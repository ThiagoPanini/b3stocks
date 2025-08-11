/* -----------------------------------------------------------------------------
  FILE: variables.tf
  MODULE: aws/get-b3-stock-tickers

  DESCRIPTION:
    Variables for configuring all infrastructure resources related to the process
    of getting active stock tickers from B3 (the Brazilian Stock Exchange).
----------------------------------------------------------------------------- */

/* --------------------------------------------------------
   VARIABLES: Lambda Function
-------------------------------------------------------- */

variable "lambda_function_name" {
  description = "Name of the Lambda function to be created for processing B3 active tickers"
  type        = string
  default     = "get-b3-stock-tickers"
}

variable "lambda_function_runtime" {
  description = "Runtime environment for the Lambda function"
  type        = string
  default     = "python3.12"
}

variable "lambda_function_architectures" {
  description = "List of architectures for the Lambda function"
  type        = list(string)
  default     = ["x86_64"]
}

variable "lambda_function_timeout_seconds" {
  description = "Timeout for the Lambda function in seconds"
  type        = number
  default     = 180

  validation {
    condition     = var.lambda_function_timeout_seconds >= 1 && var.lambda_function_timeout_seconds <= 900
    error_message = "Timeout must be between 1 second and 900 seconds (15 minutes)."
  }
}

variable "lambda_function_cron_expression" {
  description = "Cron expression for scheduling the Lambda function"
  type        = string
  default     = "cron(0 21 * * ? *)" # Runs every day at 21:00 UTC
}


/* --------------------------------------------------------
   VARIABLES: S3 Bucket
-------------------------------------------------------- */

variable "s3_bucket_name_prefix" {
  description = "Name of the S3 bucket to be created for storing B3 stock ticker data. The bucket name will be made of the value of this variable, account_id and region name ({var.s3_bucket_name_prefix}-{account_id}-{region_name})"
  type        = string
  default     = "b3stocks-bronze"

  validation {
    condition     = !endswith(var.s3_bucket_name_prefix, "-")
    error_message = "S3 bucket name prefix must not end with a dash '-'."
  }
}


/* --------------------------------------------------------
   VARIABLES: Glue Data Catalog
-------------------------------------------------------- */

variable "glue_table_name" {
  description = "Name of the Glue table to be created for storing B3 stock ticker data"
  type        = string
  default     = "tbl_dim_active_stock_tickers"

  validation {
    condition     = !contains(var.glue_table_name, "-")
    error_message = "Glue table name must not contain a dash '-'."
  }
}


/* --------------------------------------------------------
   VARIABLES: SNS Topic
-------------------------------------------------------- */

variable "sns_topic_name" {
  description = "Name of the SNS topic to be created for the get-b3-stock-tickers Lambda function"
  type        = string
  default     = "techplay-b3-stock-tickers-topic"
}

variable "sns_topic_display_name" {
  description = "Display name of the SNS topic"
  type        = string
  default     = "B3 Stock Tickers Topic"
}


/* --------------------------------------------------------
   VARIABLES: Tags
-------------------------------------------------------- */

variable "tags" {
  description = "A map of tags to assign to the resources"
  type        = map(string)
  default = {
    "Project" = "tech-playground"
  }
}
