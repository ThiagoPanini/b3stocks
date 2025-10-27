import os
from dataclasses import dataclass
from typing import Optional

from app.src.features.cross.domain.entities.notification_email_info import NotificationEmailInfo
from app.src.features.cross.domain.value_objects import NotificationType




@dataclass
class NotificationEmailInputDTO:
    """
    Data Transfer Object (DTO) for notification email input data.

    Attributes:
        message_id (str): The unique identifier for the SNS message.
        message_timestamp (str): The timestamp when the SNS message was sent.
        topic_arn (Optional[str]): The ARN of the SNS topic, if available.
        feature_name (str): The name of the feature sending the notification.
        notification_type (NotificationType): The type of notification being sent.
        email_info (NotificationEmailInfo): The information needed to send the notification email.

    """
    message_id: str
    message_timestamp: str
    topic_arn: Optional[str]
    feature_name: str
    notification_type: NotificationType
    email_info: NotificationEmailInfo
