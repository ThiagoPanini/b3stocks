/* -----------------------------------------------------------------------------
  FILE: sqs_queues.tf

  DESCRIPTION:
    This Terraform file centralizes all SQS queue configurations for the project
    utilizing a remote module from a Git repository.

  RESOURCES:

----------------------------------------------------------------------------- */


/* --------------------------------------------------------
   SQS QUEUE: fundamentus-stock-metrics
   Defines the AWS SQS Queue for the user's investment
   portfolio in a pub/sub architecture
-------------------------------------------------------- */

module "sqs_queue_fundamentus_stock_metrics" {
  source = "git::https://github.com/ThiagoPanini/tfbox.git?ref=aws/sqs-queue/v0.2.0"

  name                              = "b3stocks-fundamentus-stock-metrics"
  visibility_timeout_seconds        = 1080
  message_retention_seconds         = 3600
  delay_seconds                     = 0
  max_message_size                  = 262144
  receive_wait_time_seconds         = 2
  create_dead_letter_queue          = true
  copy_dlq_config_from_source_queue = true

  create_access_policy             = true
  access_policy_configuration_type = "inline"
  access_policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Id" : "SQSPolicy",
      "Statement" : [
        {
          "Sid" : "AllowSendMessageFromSNSTopic",
          "Effect" : "Allow",
          "Principal" : {
            "Service" : "sns.amazonaws.com"
          },
          "Action" : "SQS:SendMessage",
          "Resource" : "arn:aws:sqs:${local.region_name}:${local.account_id}:b3stocks-fundamentus-stock-metrics",
          "Condition" : {
            "ArnEquals" : {
              "aws:SourceArn" : "arn:aws:sns:${local.region_name}:${local.account_id}:b3stocks-active-stocks"
            }
          }
        }
      ]
    }
  )

}
