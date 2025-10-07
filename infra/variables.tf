/* -----------------------------------------------------------------------------
  FILE: variables.tf
  PROJECT: b3stocks

  DESCRIPTION:
    Variable definitions for configuring the b3stocks infrastructure deployment.
    These variables enable customization of resource names, Lambda function
    settings, and tagging while maintaining validation rules to ensure
    proper configuration.

  VARIABLE GROUPS:
    - S3 Bucket Configuration: Bucket name prefixes and key paths
    - Lambda Function Settings: Runtime, architecture, and timeout configurations
    - Resource Tagging: Default tags applied to all resources
----------------------------------------------------------------------------- */

/* --------------------------------------------------------
   VARIABLES: S3 Bucket Configuration
   Configurable bucket name prefixes and key paths for
   organizing data across different storage purposes.
-------------------------------------------------------- */

variable "s3_artifacts_bucket_name_prefix" {
  description = "The prefix for the S3 bucket name where artifacts are stored."
  type        = string
  default     = "b3stocks-artifacts"

  validation {
    condition     = !endswith(var.s3_artifacts_bucket_name_prefix, "-")
    error_message = "The prefix must not end with a hyphen ('-') as the complete bucket name adds it on local values."
  }
}

variable "s3_analytics_cdc_bucket_name_prefix" {
  description = "The prefix for the S3 bucket name where CDC analytics data is stored."
  type        = string
  default     = "b3stocks-analytics-cdc"

  validation {
    condition     = !endswith(var.s3_analytics_cdc_bucket_name_prefix, "-")
    error_message = "The prefix must not end with a hyphen ('-') as the complete bucket name adds it on local values."
  }
}

variable "s3_analytics_sor_bucket_name_prefix" {
  description = "The prefix for the S3 bucket name where analytics SoR data is stored."
  type        = string
  default     = "b3stocks-analytics-sor"

  validation {
    condition     = !endswith(var.s3_analytics_sor_bucket_name_prefix, "-")
    error_message = "The prefix must not end with a hyphen ('-') as the complete bucket name adds it on local values."
  }
}

variable "s3_investment_portfolios_key_prefix" {
  description = "The S3 object key (path) where the investment portfolio CSV file is stored within the artifacts bucket."
  type        = string
  default     = "investment_portfolios"

  validation {
    condition     = !endswith(var.s3_investment_portfolios_key_prefix, "/")
    error_message = "The prefix key must not end with a slash ('/') as the internal Terraform code adds it to the string."
  }
}

variable "s3_email_templates_folder_prefix" {
  description = "The S3 object key (path) where the batch processes email body template is stored within the artifacts bucket."
  type        = string
  default     = "email_templates"

  validation {
    condition     = !endswith(var.s3_email_templates_folder_prefix, "/")
    error_message = "The prefix key must not end with a slash ('/') as the internal Terraform code adds it to the string."
  }
}


/* --------------------------------------------------------
   VARIABLES: Lambda Function Configuration
   Common settings applied across all Lambda functions
   including runtime environment, architecture, and timeouts.
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
   VARIABLES: SES Configuration
   Common settings applied to SES email sending
-------------------------------------------------------- */

variable "ses_sender_email" {
  description = "The verified SES sender email address used to send emails."
  type        = string
  default     = "panini.development@gmail.com"
}

variable "ses_recipient_emails" {
  description = "A list of verified SES recipient email addresses to receive emails."
  type        = list(string)
  default = [
    "panini.development@gmail.com"
  ]
}


/* --------------------------------------------------------
   VARIABLES: Resource Tagging
   Default tags applied to all infrastructure resources
   for consistent labeling and cost tracking.
-------------------------------------------------------- */

variable "tags" {
  description = "A map of tags to assign to the resources"
  type        = map(string)
  default = {
    "Project" = "b3stocks"
  }
}
