import os
import json
from uuid import uuid4

import boto3

from app.src.features.check_batch_processes_completion.domain.interfaces.topic_adapter_interface import ITopicAdapter

from app.src.features.cross.domain.entities.batch_process import BatchProcess
from app.src.features.cross.utils.log import LogUtils
from app.src.features.cross.utils.serialization import SerializationUtils


class SNSTopicAdapter(ITopicAdapter):
    """
    Publishes messages to an AWS SNS topic.
    """

    def __init__(self):
        self.logger = LogUtils.setup_logger(name=__name__)
        self.client = boto3.client("sns", region_name=boto3.session.Session().region_name)
        self.topic_name = os.environ.get("SNS_BATCH_PROCESSES_COMPLETION_TOPIC_NAME")
        self.topic_arn = self.__get_topic_arn()


    def __get_topic_arn(self) -> str:
        """
        Retrieves the SNS topic ARN from environment variables and session information.
        
        Returns:
            str: The SNS topic ARN.
        """
        # Getting topic attributes needed to construct the ARN
        account_id = boto3.client("sts").get_caller_identity()["Account"]
        region_name = boto3.session.Session().region_name
        
        return f"arn:aws:sns:{region_name}:{account_id}:{self.topic_name}"


    def publish_message(self, message: BatchProcess) -> None:
        """
        Publishes a message to a SNS topic.

        Args:
            message (BatchProcess): The message to publish.
        """

        try:
            self.client.publish(
                TopicArn=self.topic_arn,
                Message=json.dumps(SerializationUtils.json_serialize(message))
            )
        except Exception:
            self.logger.exception(f"Error publishing message to SNS topic {self.topic_arn}")
            raise
