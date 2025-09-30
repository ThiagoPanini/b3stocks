from typing import Any
from dataclasses import dataclass

from app.src.features.send_batch_completion_emails.domain.dtos.input_dto import InputDTO
from app.src.features.send_batch_completion_emails.domain.interfaces.email_service_adapter_interface import (
    IEmailServiceAdapter
)
from app.src.features.send_batch_completion_emails.domain.interfaces.email_body_template_request_adapter_interface import (
    IEMailBodyTemplateRequestAdapter
)
from app.src.features.send_batch_completion_emails.domain.entities.email_body import EmailBody
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


    def execute(self, input_dto: InputDTO) -> OutputDTO:
        """
        Implements the logic to execute the use case.

        Args:
            input_dto (InputDTO): The input DTO containing event records.

        Returns:
            OutputDTO: An instance of OutputDTO containing the result of the operation.
        """
        try:
            logger.info(f"Fetching email body template from {input_dto.template_endpoint}")
            email_body: EmailBody = self.email_body_template_request_adapter.get_email_body_template(
                input_dto.template_endpoint
            )
            print(email_body)
        except Exception:
            logger.exception(f"Error fetching email body template")
            raise

        # Build mail config entity
        # Send mail using mail service adapter

        return OutputDTO.ok(
            data={
                "OK": True
            }
        )
