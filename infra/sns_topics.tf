/* -----------------------------------------------------------------------------
  FILE: sns_topics.tf

  DESCRIPTION:
    This Terraform file centralizes all SNS topic configurations for the project
    utilizing a remote module from a Git repository.

  RESOURCES:
    
----------------------------------------------------------------------------- */

/* --------------------------------------------------------
   SNS TOPIC: active-stocks
   Defines the AWS SNS Topic for the user's investment
   portfolio in a pub/sub architecture
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
      endpoint               = "arn:aws:sqs:${local.region_name}:${local.account_id}:b3stocks-fundamentus-stock-metrics"
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
