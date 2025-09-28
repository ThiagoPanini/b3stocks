/* -----------------------------------------------------------------------------
  FILE: ses.tf
  PROJECT: b3stocks

  DESCRIPTION:
    This Terraform file provisions AWS Simple Email Service (SES) resources
    for the b3stocks project. It configures email sending capabilities including
    domain/email verification, configuration sets, and IAM permissions for
    Lambda functions to send HTML emails for batch process notifications.

  RESOURCES:
    - SES Domain Identity: Domain verification for email sending
    - SES Email Identity: Individual email address verification
    - SES Configuration Set: Email sending configuration and tracking
    - IAM Policy: Permissions for Lambda functions to send emails
----------------------------------------------------------------------------- */

/* --------------------------------------------------------
   SES DOMAIN IDENTITY (Optional)
   Verifies a domain for sending emails. This is optional
   and only needed if you want to send emails from a
   custom domain (e.g., noreply@yourdomain.com).
   
   To use this, uncomment and update the domain variable.
-------------------------------------------------------- */

# variable "ses_domain" {
#   description = "Domain to verify for SES email sending"
#   type        = string
#   default     = "yourdomain.com"
# }

# resource "aws_ses_domain_identity" "main" {
#   domain = var.ses_domain
# }

# resource "aws_ses_domain_dkim" "main" {
#   domain = aws_ses_domain_identity.main.domain
# }

# # Domain verification record (you need to add this to your DNS)
# resource "aws_route53_record" "ses_verification" {
#   count   = var.ses_domain != "" ? 1 : 0
#   zone_id = "YOUR_HOSTED_ZONE_ID"  # Update with your Route53 hosted zone ID
#   name    = "_amazonses.${var.ses_domain}"
#   type    = "TXT"
#   ttl     = 600
#   records = [aws_ses_domain_identity.main.verification_token]
# }

/* --------------------------------------------------------
   SES EMAIL IDENTITY
   Verifies individual email addresses for sending emails.
   This is the simplest approach for testing and development.
   You can verify multiple email addresses as needed.
-------------------------------------------------------- */

variable "ses_verified_emails" {
  description = "List of email addresses to verify for SES sending"
  type        = list(string)
  default = [
    "panini.development@gmail.com"
    # Add your email addresses here for verification
    # "noreply@yourdomain.com",
    # "admin@yourdomain.com"
  ]
}

resource "aws_ses_email_identity" "verified_emails" {
  count = length(var.ses_verified_emails)
  email = var.ses_verified_emails[count.index]
}

/* --------------------------------------------------------
   SES CONFIGURATION SET
   Creates a configuration set for organizing email sending
   and tracking delivery statistics. This is optional but
   recommended for production environments.
-------------------------------------------------------- */

resource "aws_ses_configuration_set" "b3stocks" {
  name = "b3stocks-email-config"

  # Optional: Track delivery events
  delivery_options {
    tls_policy = "Require" # Enforce TLS encryption
  }
}

# Event destination for tracking email events (optional)
resource "aws_ses_event_destination" "cloudwatch" {
  name                   = "cloudwatch-destination"
  configuration_set_name = aws_ses_configuration_set.b3stocks.name
  enabled                = true
  matching_types = [
    "send",
    "reject",
    "bounce",
    "complaint",
    "delivery"
  ]

  cloudwatch_destination {
    default_value  = "default"
    dimension_name = "EmailAddress"
    value_source   = "messageTag"
  }
}

/* --------------------------------------------------------
   IAM POLICY: SES Send Email Permissions
   Creates an IAM policy that allows Lambda functions to
   send emails using SES. This policy will be attached to
   Lambda execution roles that need email sending capabilities.
-------------------------------------------------------- */
/*
data "aws_iam_policy_document" "ses_send_email" {
  statement {
    sid    = "AllowSESSendEmail"
    effect = "Allow"

    actions = [
      "ses:SendEmail",
      "ses:SendRawEmail",
      "ses:SendBulkTemplatedEmail",
      "ses:SendTemplatedEmail"
    ]

    resources = [
      # Allow sending from verified email identities
      "arn:aws:ses:${data.aws_region.current.name}:${local.account_id}:identity/*",
      # Allow sending through configuration set
      "arn:aws:ses:${data.aws_region.current.name}:${local.account_id}:configuration-set/${aws_ses_configuration_set.b3stocks.name}"
    ]

    condition {
      test     = "StringEquals"
      variable = "ses:FromAddress"
      values   = var.ses_verified_emails
    }
  }

  statement {
    sid    = "AllowSESGetSendQuota"
    effect = "Allow"

    actions = [
      "ses:GetSendQuota",
      "ses:GetSendStatistics",
      "ses:GetAccountSendingEnabled"
    ]

    resources = ["*"]
  }
}

resource "aws_iam_policy" "ses_send_email" {
  name        = "b3stocks-ses-send-email-policy"
  path        = "/"
  description = "IAM policy allowing Lambda functions to send emails via SES"

  policy = data.aws_iam_policy_document.ses_send_email.json

  tags = var.tags
}

/* --------------------------------------------------------
   IAM ROLE ATTACHMENT: Check Batch Processes Completion
   Attaches the SES send email policy to the batch completion
   Lambda function role, enabling it to send notification emails.
-------------------------------------------------------- */
/*
# Get the existing Lambda execution role for batch completion
data "aws_iam_role" "lambda_check_batch_processes_completion" {
  name = "role-b3stocks-lambda-check-batch-processes-completion"

  depends_on = [
    # Ensure this runs after the role is created in iam_roles.tf
  ]
}

resource "aws_iam_role_policy_attachment" "lambda_batch_completion_ses" {
  role       = data.aws_iam_role.lambda_check_batch_processes_completion.name
  policy_arn = aws_iam_policy.ses_send_email.arn
}
*/

/* --------------------------------------------------------
   OUTPUTS: SES Resource Information
   Export important SES resource details for use in
   other Terraform modules or for reference.
-------------------------------------------------------- */

output "ses_configuration_set_name" {
  description = "Name of the SES configuration set"
  value       = aws_ses_configuration_set.b3stocks.name
}

output "ses_verified_emails" {
  description = "List of verified email addresses"
  value       = var.ses_verified_emails
}


/* --------------------------------------------------------
   LOCAL VALUES: SES Environment Variables
   Define environment variables that should be added to
   Lambda functions that need to send emails.
-------------------------------------------------------- */

locals {
  ses_environment_variables = {
    SES_CONFIGURATION_SET_NAME = aws_ses_configuration_set.b3stocks.name
    SES_FROM_EMAIL             = length(var.ses_verified_emails) > 0 ? var.ses_verified_emails[0] : ""
    SES_REGION                 = data.aws_region.current.name
  }
}

/* --------------------------------------------------------
   NOTES FOR SETUP AND TESTING:
   
   1. EMAIL VERIFICATION (Required):
      - Add your email addresses to `ses_verified_emails` variable
      - After applying Terraform, check your email for verification links
      - Click the verification links to activate email sending
   
   2. SANDBOX MODE (Default):
      - New AWS accounts start in SES sandbox mode
      - You can only send emails to verified addresses
      - To send to any email address, request production access:
        AWS Console > SES > Account dashboard > Request production access
   
   3. DOMAIN VERIFICATION (Optional):
      - Uncomment domain-related resources if using custom domain
      - Add DNS records to verify domain ownership
      - Update Route53 hosted zone ID in the configuration
   
   4. TESTING THE CONFIGURATION:
      - Use the sample script: sample_html_email_script.py
      - Update CONFIG values with your verified email addresses
      - Ensure your Lambda functions have the SES policy attached
   
   5. ENVIRONMENT VARIABLES:
      - Add `ses_environment_variables` to your Lambda functions
      - These provide SES configuration to your application code
   
   6. MONITORING (Optional):
      - CloudWatch event destination tracks email metrics
      - View delivery statistics in AWS CloudWatch console
      - Monitor bounce rates and complaint rates
-------------------------------------------------------- */
