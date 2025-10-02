from typing import Any

from app.src.features.send_batch_completion_emails.infra.mappers.sns_event_lambda_mapper import (
    SNSEventLambdaMapper
)
from app.src.features.send_batch_completion_emails.infra.adapters.s3_email_body_template_request_adapter import (
    S3MailBodyTemplateAdapter
)
from app.src.features.send_batch_completion_emails.infra.adapters.ses_mail_service_adapter import (
    SESMailServiceAdapter
)
from app.src.features.send_batch_completion_emails.use_case.send_batch_processes_emails_use_case import (
    SendBatchCompletionEMailsUseCase
)
from app.src.features.cross.infra.mappers.http_response_mapper import HTTPResponseMapper


# Initializing mappers, adapters and repositories
event_mapper = SNSEventLambdaMapper()
email_body_template_request_adapter = S3MailBodyTemplateAdapter()
email_service_adapter = SESMailServiceAdapter()


# Initializing use case
use_case = SendBatchCompletionEMailsUseCase(
    email_body_template_request_adapter=email_body_template_request_adapter,
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

    input_dto = event_mapper.map_event_to_input_dto(event=event)
    output_dto = use_case.execute(input_dto=input_dto)

    return HTTPResponseMapper.map(output_dto)