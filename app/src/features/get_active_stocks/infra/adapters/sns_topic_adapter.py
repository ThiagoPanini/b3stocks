import os
import json
from uuid import uuid4

import boto3

from app.src.features.get_active_stocks.domain.interfaces.topic_adapter_interface import ITopicAdapter

from app.src.features.cross.domain.entities.stock_message import StockMessage
from app.src.features.cross.utils.log import LogUtils
from app.src.features.cross.utils.serialization import SerializationUtils
from app.src.features.cross.utils.decorators import timing_decorator


class SNSTopicAdapter(ITopicAdapter):
    """
    Publishes messages to an AWS SNS topic.
    """

    def __init__(self):
        self.logger = LogUtils.setup_logger(name=__name__)
        self.client = boto3.client("sns", region_name=boto3.session.Session().region_name)
        self.topic_name = os.environ.get("SNS_ACTIVE_STOCKS_TOPIC_NAME")
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

    
    @timing_decorator
    def batch_publish_messages(self, messages: list[StockMessage]) -> None:
        """
        Publishes a batch of messages to a SNS topic.

        Args:
            messages (list[StockMessage]): A list of messages to publish.
        """
        
        # Preparing messages to be sent in batches
        try:
            entries = [
                {
                    "Id": str(uuid4()),
                    "Message": json.dumps(SerializationUtils.json_serialize(message))
                }
                for message in messages
            ]
        except Exception as e:
            self.logger.error(f"Error preparing messages for batch publish into a SNS topic: {e}")
            raise

        # Sending messages in batches of 10 messages per batch
        try:
            for i in range(0, len(entries), 10):
                batch_entries = entries[i:i + 10]

                _ = self.client.publish_batch(
                    TopicArn=self.topic_arn,
                    PublishBatchRequestEntries=batch_entries
                )

                # Logging the loop status
                LogUtils.log_loop_status(
                    logger=self.logger,
                    loop_idx=i // 10,
                    total_elements=len(messages) // 10,
                    log_pace=20,
                    log_msg=f"Published {i // 10} batches of 10 messages each to topic"
                )

        except Exception:
            self.logger.exception("Error publishing batch messages to SNS")
            raise
        else:
            self.logger.info(f"Successfully published messages to SNS topic {self.topic_arn}")
