/* -----------------------------------------------------------------------------
  FILE: sns_topics.tf
  PROJECT: b3stocks

  DESCRIPTION:
    This Terraform file defines SNS topics for the b3stocks project messaging
    architecture. Topics enable decoupled communication between services using
    a publish-subscribe pattern with proper encryption and access controls.

  TOPICS:
    - b3stocks-active-stocks: Publishes active stock events to downstream subscribers
----------------------------------------------------------------------------- */

/* --------------------------------------------------------
   SNS TOPIC: b3stocks-active-stocks
   Publishes active stock events to enable downstream processing.
   Configured with AWS managed KMS encryption and subscribes
   to SQS queue for Fundamentus stock metrics processing.
-------------------------------------------------------- */

module "sns_topic_active_stocks" {
  source = "git::https://github.com/ThiagoPanini/tfbox.git?ref=aws/sns-topic/v0.0.1"

  name         = "b3stocks-active-stocks"
  display_name = "B3 Active Stocks"

  kms_master_key_id = data.aws_kms_key.sns.id

  create_topic_policy = true
  topic_policy = jsonencode(
    {
      "Version" : "2008-10-17",
      "Statement" : [
        {
          "Sid" : "SNSTopicPolicy",
          "Effect" : "Allow",
          "Principal" : {
            "AWS" : "*"
          },
          "Action" : [
            "SNS:GetTopicAttributes",
            "SNS:SetTopicAttributes",
            "SNS:AddPermission",
            "SNS:RemovePermission",
            "SNS:DeleteTopic",
            "SNS:Subscribe",
            "SNS:ListSubscriptionsByTopic",
            "SNS:Publish"
          ],
          "Resource" : "arn:aws:sns:${local.region_name}:${local.account_id}:b3stocks-active-stocks",
          "Condition" : {
            "StringEquals" : {
              "AWS:SourceOwner" : "${local.account_id}"
            }
          }
        }
      ]
    }
  )

  subscriptions = [
    {
      protocol               = "sqs"
      endpoint               = "arn:aws:sqs:${local.region_name}:${local.account_id}:b3stocks-fundamentus-eod-stock-metrics"
      endpoint_auto_confirms = true
      raw_message_delivery   = false
    }
  ]
}

/*
ToDo:
  - Refine topic policy to restrict access to specific AWS accounts or services, such as:
    - Only allow publishing from the Lambda function's role.
    - Only allow subscriptions from specific SQS queues.
*/
