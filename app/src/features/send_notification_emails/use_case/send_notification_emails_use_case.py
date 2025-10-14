from dataclasses import dataclass

from app.src.features.send_notification_emails.domain.dtos.notification_email_input_dto import (
    NotificationEmailInputDTO
)
from app.src.features.send_notification_emails.domain.interfaces.email_service_adapter_interface import (
    IEmailServiceAdapter
)
from app.src.features.cross.domain.entities.notification_email_info import NotificationEmailInfo
from app.src.features.cross.domain.entities.notification_email_template_setup import (
    NotificationEmailTemplateSetup
)

from app.src.features.cross.utils.log import LogUtils
from app.src.features.cross.domain.dtos.output_dto import OutputDTO


logger = LogUtils.setup_logger(name=__name__)


@dataclass
class SendNotificationEmailsUseCase:
    """
    Use case for sending notification emails.
    """
    email_service_adapter: IEmailServiceAdapter


    def execute(self, input_dto: NotificationEmailInputDTO) -> OutputDTO:
        """
        Implements the logic to execute the use case.

        Args:
            input_dto (NotificationEmailInputDTO): The input DTO containing event records.

        Returns:
            OutputDTO: An instance of OutputDTO containing the result of the operation.
        """
        email_info: NotificationEmailInfo = input_dto.email_info
        template_setup: NotificationEmailTemplateSetup = email_info.template_setup

        try:
            logger.info(f"Fetching email body template from {template_setup.template_endpoint_url}")
            email_body_html: str = self.email_service_adapter.fetch_email_html_template(
                template_endpoint=template_setup.template_endpoint_url
            )
            logger.info("Successfully fetched email body template")
        except Exception:
            logger.exception(f"Error fetching email body template from {template_setup.template_endpoint_url}")
            raise

        try:
            logger.info("Replacing email body template placeholders with actual values")
            email_body_filled: str = self.email_service_adapter.replace_email_html_template_placeholders(
                template=email_body_html,
                placeholders=template_setup.template_placeholders
            )
            logger.info("Successfully replaced email body template placeholders with actual values")
        except Exception:
            logger.exception("Error replacing email body template placeholders with actual values")
            raise

        try:
            logger.info(f"Sending notification email to {', '.join(email_info.recipients)}")
            self.email_service_adapter.send_email(
                subject=email_info.subject,
                body_html=email_body_filled,
                sender=email_info.sender,
                recipients=email_info.recipients,
                reply_to_addresses=email_info.reply_to_addresses
            )
            logger.info(f"Successfully sent notification email to {', '.join(email_info.recipients)}")
        except Exception:
            logger.exception(f"Error sending notification email to {', '.join(email_info.recipients)}")
            raise

        return OutputDTO.ok(
            data={
                "message": f"Notification email sent to {', '.join(email_info.recipients)}"
            }
        )
