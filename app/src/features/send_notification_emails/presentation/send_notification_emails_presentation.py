from typing import Any

from app.src.features.send_notification_emails.infra.mappers.sns_notification_email_event_mapper import (
    SNSNotificationEmailEventMapper
)
from app.src.features.send_notification_emails.infra.adapters.ses_email_service_adapter import (
    SESEmailServiceAdapter
)
from app.src.features.send_notification_emails.use_case.send_notification_emails_use_case import (
    SendNotificationEmailsUseCase
)
from app.src.features.cross.infra.mappers.http_response_mapper import HTTPResponseMapper
from app.src.features.cross.utils.env import EnvironmentVarsUtils


# Initializing mappers, adapters and repositories
event_mapper = SNSNotificationEmailEventMapper()
email_service_adapter = SESEmailServiceAdapter()


# Initializing use case
use_case = SendNotificationEmailsUseCase(
    email_service_adapter=email_service_adapter
)


# Defining a handler function for executing the use case in AWS Lambda
def handler(event: dict[str, Any], context: Any = None) -> dict:
    """
    AWS Lambda handler function to execute the use case.

    Args:
        event (dict[str, Any]): The event data passed to the Lambda function.
        context (Any): The context object provided by AWS Lambda.

    Returns:
        dict: The result of the use case execution, typically a B3InvestmentPortfolioRequest instance.
    """

    EnvironmentVarsUtils.check_required_env_vars(
        required_env_vars=[
            "S3_ARTIFACTS_BUCKET_NAME_PREFIX",
            "S3_EMAIL_TEMPLATES_FOLDER_PREFIX",
            "SES_SENDER_EMAIL",
            "SES_RECIPIENT_EMAILS"
        ]
    )

    input_dto = event_mapper.map_event_to_input_dto(event=event)
    output_dto = use_case.execute(input_dto=input_dto)

    return HTTPResponseMapper.map(output_dto)