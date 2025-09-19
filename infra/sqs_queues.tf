/* -----------------------------------------------------------------------------
  FILE: sqs_queues.tf
  PROJECT: b3stocks

  DESCRIPTION:
    This Terraform file defines SQS queues for the b3stocks project messaging
    infrastructure. Queues provide reliable message delivery and buffering
    between services with appropriate access policies and dead letter queues
    for error handling.

  QUEUES:
    - b3stocks-fundamentus-eod-stock-metrics: Receives messages from SNS topic for processing
----------------------------------------------------------------------------- */


/* --------------------------------------------------------
   SQS QUEUE: b3stocks-fundamentus-eod-stock-metrics
   Receives messages from active stocks SNS topic to trigger
   Fundamentus stock metrics collection. Configured with
   appropriate timeouts and dead letter queue for error handling.
-------------------------------------------------------- */

module "sqs_queue_fundamentus_eod_stock_metrics" {
  source = "git::https://github.com/ThiagoPanini/tfbox.git?ref=aws/sqs-queue/v0.2.0"

  name                              = "b3stocks-fundamentus-eod-stock-metrics"
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
          "Resource" : "arn:aws:sqs:${local.region_name}:${local.account_id}:b3stocks-fundamentus-eod-stock-metrics",
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
