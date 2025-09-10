/* -----------------------------------------------------------------------------
  FILE: variables.tf
  MODULE: aws/get-investment-portfolio

  DESCRIPTION:
    Variables for configuring all infrastructure resources related to the process
    of getting investment portfolio data from an user given source.
----------------------------------------------------------------------------- */

/* --------------------------------------------------------
   VARIABLES: S3 Buckets
-------------------------------------------------------- */

variable "s3_investment_portfolio_object_key" {
  description = "The S3 object key (path) where the investment portfolio CSV file is stored within the artifacts bucket."
  type        = string
  default     = "investment_portfolio/b3_investment_portfolio.yaml"

}


/* --------------------------------------------------------
   VARIABLES: Lambda Function
   Common settings that can be applied to all Lambda
   functions in this project.
-------------------------------------------------------- */

variable "lambda_function_common_runtime" {
  description = "Runtime environment for the Lambda function"
  type        = string
  default     = "python3.12"
}

variable "lambda_function_common_architectures" {
  description = "List of architectures for the Lambda function"
  type        = list(string)
  default     = ["x86_64"]
}

variable "lambda_function_common_timeout_seconds" {
  description = "Timeout for the Lambda function in seconds"
  type        = number
  default     = 180

  validation {
    condition     = var.lambda_function_common_timeout_seconds >= 1 && var.lambda_function_common_timeout_seconds <= 900
    error_message = "Timeout must be between 1 second and 900 seconds (15 minutes)."
  }
}


/* --------------------------------------------------------
   VARIABLES: Tags
   Tags to apply to all resources
-------------------------------------------------------- */

variable "tags" {
  description = "A map of tags to assign to the resources"
  type        = map(string)
  default = {
    "Project" = "b3stocks"
  }
}
