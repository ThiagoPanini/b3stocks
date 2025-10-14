from typing import Any
import json
import os
from datetime import datetime

import boto3

from app.src.features.cross.domain.entities.notification_email_info import NotificationEmailInfo
from app.src.features.cross.domain.entities.notification_email_template_setup import (
    NotificationEmailTemplateSetup
)
from app.src.features.send_notification_emails.domain.dtos.notification_email_input_dto import (
    NotificationEmailInputDTO
)
from app.src.features.cross.domain.value_objects import NotificationType
from app.src.features.cross.utils.aws_client import AWSClient
from app.src.features.cross.utils.log import LogUtils


logger = LogUtils.setup_logger(name=__name__)


class SNSNotificationEmailEventMapper:
    """
    Maps a SNS event dict to a input Data Transfer Object (DTO) class
    """

    def __build_template_endpoint_url(self, notification_type: NotificationType) -> str:
        """
        Builds the S3 URI for the HTML email template based on the notification type.

        Args:
            notification_type (NotificationType): The type of notification (e.g., SUCCESS, FAILURE).
        
        Returns:
            str: The S3 URI of the HTML email template.
        """
        bucket_name = AWSClient.build_bucket_name_from_prefix(
            bucket_name_prefix=os.getenv("S3_ARTIFACTS_BUCKET_NAME_PREFIX")
        )
        folder_prefix = os.getenv("S3_EMAIL_TEMPLATES_FOLDER_PREFIX").strip("/")
        object_key = f"{folder_prefix}/b3stocks_{notification_type.value.lower()}_notification.html"

        return f"s3://{bucket_name}/{object_key}"


    def __build_notification_email_subject(self, feature_name: str, notification_type: NotificationType) -> str:
        """
        Builds the email subject by prepending the feature name to the base subject.

        Args:
            feature_name (str): The name of the feature sending the notification.
            notification_type (NotificationType): The type of notification being sent.

        Returns:
            str: The constructed email subject.
        """
        feature_name = feature_name.strip().upper()
        if notification_type == NotificationType.SUCCESS:
            subject = f"✅ b3stocks [{feature_name}] Completed Successfully"
        else:
            subject = f"❌ b3stocks [{feature_name}] Failed"

        return subject


    def map_event_to_input_dto(self, event: dict[str, Any]) -> NotificationEmailInputDTO:
        """
        Maps a SNS Lambda event dict to a input Data Transfer Object (DTO) class

        Args:
            event (dict): The AWS Lambda event dict received from SNS.

        Returns:
            NotificationEmailInputDTO: The mapped input Data Transfer Object.
        """
        records = event.get("Records", [])
        if not records:
            raise ValueError("No records found in source event")
        
        try:
            # Taking the record from the event and mapping to BatchProcess entity
            sns_record = records[0].get("Sns", {})
            message = json.loads(sns_record.get("Message", "{}"))

            # Getting the notification type and other info that depends on it
            notification_type: NotificationType = NotificationType(message.get("notification_type"))
            template_endpoint_url: str = self.__build_template_endpoint_url(
                notification_type=notification_type
            )
            email_subject: str = self.__build_notification_email_subject(
                feature_name=message.get("feature_name"),
                notification_type=notification_type
            )

            # Building an input DTO instance
            input_dto = NotificationEmailInputDTO(
                message_id=sns_record.get("MessageId"),
                message_timestamp=sns_record.get("Timestamp"),
                topic_arn=sns_record.get("TopicArn"),
                feature_name=message.get("feature_name"),
                notification_type=notification_type,
                email_info=NotificationEmailInfo(
                    sender=os.getenv("SES_SENDER_EMAIL"),
                    recipients=json.loads(os.getenv("SES_RECIPIENT_EMAILS")),
                    subject=email_subject,
                    template_setup=NotificationEmailTemplateSetup(
                        template_endpoint_url=template_endpoint_url,
                        template_placeholders=message.get("template_placeholders", {})
                    )
                )
            )

            return input_dto

        except json.JSONDecodeError:
            logger.exception("Invalid JSON format in SNS message")
            raise
            
        except TypeError:
            logger.exception(f"Error mapping SNS message to BatchProcess entity")
            raise

        except Exception:
            logger.exception("Unexpected error while mapping event to InputDTO")
            raise
