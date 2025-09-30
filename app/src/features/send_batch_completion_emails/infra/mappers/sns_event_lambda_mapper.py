from typing import Any
import json
import os

import boto3

from app.src.features.send_batch_completion_emails.domain.dtos.input_dto import InputDTO
from app.src.features.cross.domain.entities.batch_process import BatchProcess
from app.src.features.cross.utils.log import LogUtils


logger = LogUtils.setup_logger(name=__name__)


class SNSEventLambdaMapper:
    """
    Maps a SNS Lambda event dict to a input Data Transfer Object (DTO) class
    """

    def __build_bucket_name_from_prefix(self, bucket_name_prefix: str) -> str:
        """
        Constructs the full S3 bucket name using the provided prefix and environment variables.

        Args:
            bucket_name_prefix (str): The prefix for the S3 bucket name.
        
        Returns:
            str: The constructed S3 bucket name.
        """
        account_id = boto3.client("sts").get_caller_identity()["Account"]
        region_name = boto3.session.Session().region_name

        return f"{bucket_name_prefix}-{account_id}-{region_name}"


    def map_event_to_input_dto(self, event: dict[str, Any]) -> InputDTO:
        """
        Maps a SNS Lambda event dict to a input Data Transfer Object (DTO) class

        Args:
            event (dict): The AWS Lambda event dict received from SNS.

        Returns:
            InputDTO: The mapped input Data Transfer Object.
        """

        # Checking if environment variables exists and if not, raise an error
        bucket_name_prefix = os.getenv("S3_ARTIFACTS_BUCKET_NAME_PREFIX") 
        object_key = os.getenv("S3_BATCH_PROCESSES_EMAIL_BODY_TEMPLATE_OBJECT_KEY")
        if not bucket_name_prefix or not object_key:
            raise EnvironmentError(
                "Required environment variables are missing: 'S3_ARTIFACTS_BUCKET_NAME_PREFIX' "
                "and 'S3_BATCH_PROCESSES_EMAIL_BODY_TEMPLATE_OBJECT_KEY'"
            )

        records = event.get("Records", [])
        if not records:
            raise ValueError("No records found in source event")

        try:
            # Taking the record from the event and mapping to BatchProcess entity
            sns_record = records[0].get("Sns", {})
            message = sns_record.get("Message", "{}")
            batch_process = BatchProcess(**json.loads(message))

            # Constructing InputDTO
            template_endpoint_bucket_name = self.__build_bucket_name_from_prefix(bucket_name_prefix)
            input_dto = InputDTO(
                template_endpoint=f"s3://{template_endpoint_bucket_name}/{object_key}",
                batch_process=batch_process
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
