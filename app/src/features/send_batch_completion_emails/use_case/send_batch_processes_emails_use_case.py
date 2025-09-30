import os
from dataclasses import dataclass

from app.src.features.send_batch_completion_emails.domain.dtos.input_dto import InputDTO
from app.src.features.send_batch_completion_emails.domain.interfaces.email_service_adapter_interface import (
    IEmailServiceAdapter
)
from app.src.features.send_batch_completion_emails.domain.interfaces.email_body_template_request_adapter_interface import (
    IEMailBodyTemplateRequestAdapter
)
from app.src.features.send_batch_completion_emails.domain.entities.email_body import EmailBody
from app.src.features.send_batch_completion_emails.domain.entities.email_setup import EmailSetup
from app.src.features.send_batch_completion_emails.domain.entities.email_placeholders import EmailPlaceholders
from app.src.features.cross.utils.log import LogUtils
from app.src.features.cross.domain.dtos.output_dto import OutputDTO


logger = LogUtils.setup_logger(name=__name__)


@dataclass(frozen=True)
class SendBatchCompletionEMailsUseCase:
    """
    Use case for checking the completion of batch processes related to stock metrics.
    """

    # email_service_adapter: IMailServiceAdapter
    email_body_template_request_adapter: IEMailBodyTemplateRequestAdapter


    def __check_env_variables(self) -> None:
        """
        Checks if the required environment variables are set.

        Raises:
            EnvironmentError: If any required environment variable is missing.
        """
        required_env_vars = [
            "SES_SENDER_EMAIL",
            "SES_RECIPIENT_EMAILS"
        ]

        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        if missing_vars:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    
    def execute(self, input_dto: InputDTO) -> OutputDTO:
        """
        Implements the logic to execute the use case.

        Args:
            input_dto (InputDTO): The input DTO containing event records.

        Returns:
            OutputDTO: An instance of OutputDTO containing the result of the operation.
        """
        self.__check_env_variables()

        try:
            logger.info(f"Fetching email body template from {input_dto.template_endpoint}")
            email_body: EmailBody = self.email_body_template_request_adapter.get_email_body_template(
                input_dto.template_endpoint
            )
            logger.info("Successfully fetched email body template")
        except Exception:
            logger.exception(f"Error fetching email body template from {input_dto.template_endpoint}")
            raise

        try:
            email_setup: EmailSetup = EmailSetup(
                subject=f"🏦 b3stocks | Batch Process '{input_dto.batch_process.name}' {input_dto.batch_process.status}",
                sender=os.getenv("SES_SENDER_EMAIL"),
                recipients=os.getenv("SES_RECIPIENT_EMAILS").split(","),
                body=email_body,
            )
        except TypeError:
            logger.exception("Error building email setup entity")
            raise

        try:
            # TODO: Isn't this the same as the BatchProcess entity?
            email_placeholders: EmailPlaceholders = EmailPlaceholders(
                batch_process_name=input_dto.batch_process.name,
                batch_process_status=input_dto.batch_process.status,
                batch_process_start_time=str(input_dto.batch_process.start_time),
                batch_process_end_time=str(input_dto.batch_process.end_time),
                batch_process_details=input_dto.batch_process.details or "N/A"
            )
        except TypeError:
            logger.exception("Error building email placeholders entity")
            raise

        # Send mail using email service adapter

        return OutputDTO.ok(
            data={
                "OK": True
            }
        )
