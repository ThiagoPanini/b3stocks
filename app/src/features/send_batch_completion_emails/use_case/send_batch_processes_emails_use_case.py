import json
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any

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
from app.src.features.cross.domain.entities.batch_process import BatchProcess
from app.src.features.cross.utils.log import LogUtils
from app.src.features.cross.domain.dtos.output_dto import OutputDTO


logger = LogUtils.setup_logger(name=__name__)


@dataclass(frozen=True)
class SendBatchCompletionEMailsUseCase:
    """
    Use case for checking the completion of batch processes related to stock metrics.
    """

    email_body_template_request_adapter: IEMailBodyTemplateRequestAdapter
    email_service_adapter: IEmailServiceAdapter

    
    def execute(self, input_dto: InputDTO) -> OutputDTO:
        """
        Implements the logic to execute the use case.

        Args:
            input_dto (InputDTO): The input DTO containing event records.

        Returns:
            OutputDTO: An instance of OutputDTO containing the result of the operation.
        """

        batch_process: BatchProcess = input_dto.batch_process
        try:
            logger.info(f"Fetching email body template from {input_dto.template_endpoint}")
            email_body: EmailBody = self.email_body_template_request_adapter.get_email_body_template(
                input_dto.template_endpoint
            )
            logger.info("Successfully fetched email body template")

            process_name: str = " ".join(word.capitalize() for word in batch_process.process_name.value.split("_"))
            process_status: str = batch_process.process_status.value.replace(" ", "_").capitalize()
            email_setup: EmailSetup = EmailSetup(
                subject=f"💰 b3stocks | {process_status} {process_name}",
                sender=os.getenv("SES_SENDER_EMAIL"),
                recipients=[
                    os.getenv("SES_SENDER_EMAIL")  # The sender also receives the email
                ],
                body=email_body
            )

            email_placeholders: dict[str, Any] = {
                "batch_process_name": batch_process.process_name.value,
                "completion_status": batch_process.process_status.value,
                "execution_date": str(batch_process.execution_date),
                "current_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_records": str(batch_process.total_items),
                "execution_time": "teste"
            }
            self.email_service_adapter.send_email(
                email_setup=email_setup,
                replace_placeholders=True,
                placeholders=email_placeholders
            )
            logger.info(f"Successfully sent completion email to {email_setup.recipients}")
        
        except TypeError:
            logger.exception("Error building email setup or sending email due to type mismatch")
            raise

        except Exception:
            logger.exception("Error executing the use case for sending batch completion emails")
            raise

        return OutputDTO.ok(
            data={
                "email_sender": email_setup.sender,
                "email_recipients": email_setup.recipients,
            }
        )
