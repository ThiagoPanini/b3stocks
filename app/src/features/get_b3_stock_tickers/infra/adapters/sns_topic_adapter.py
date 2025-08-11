import os
import json
from uuid import uuid4

import boto3

from app.src.features.cross.utils.decorators import timing_decorator
from app.src.features.cross.utils.log_utils import (
    setup_logger,
    log_loop_status
)
from app.src.features.get_b3_stock_tickers.domain.interfaces.topic_adapter_interface import (
    ITopicAdapter
)
from app.src.features.get_b3_stock_tickers.domain.entities.b3_stock_ticker_message import (
    B3StockTickerMessage
)


class SNSTopicAdapter(ITopicAdapter):
    """
    Publishes messages to an AWS SNS topic.
    """

    def __init__(self):
        self.logger = setup_logger(__name__)
        self.client = boto3.client("sns", region_name=boto3.session.Session().region_name)

    def __get_topic_arn(self) -> str:
        """
        Retrieves the SNS topic ARN from environment variables and session information.
        
        Returns:
            str: The SNS topic ARN.
        """
        # Getting topic attributes needed to construct the ARN
        account_id = boto3.client("sts").get_caller_identity()["Account"]
        region_name = boto3.session.Session().region_name
        topic_name = os.environ.get("SNS_B3_STOCK_TICKERS_TOPIC_NAME")
        
        return f"arn:aws:sns:{region_name}:{account_id}:{topic_name}"
    
    @timing_decorator
    def publish_messages(self, messages: list[B3StockTickerMessage]) -> None:
        """
        Publishes a list of messages to the topic.

        Args:
            messages (list[B3StockTickerMessage]): The messages to publish (should be serializable).
        """

        # Getting account ID from

        try:
            for idx, message in enumerate(messages):
                self.client.publish(
                    TopicArn=self.topic_arn,
                    Message=json.dumps(
                        message.message_body.__dict__,
                    )
                )

                # Logging the loop status
                log_loop_status(
                    logger=self.logger,
                    loop_idx=idx,
                    total_elements=len(messages),
                    log_pace=100,
                    log_msg=f"Published {idx} messages to topic"
                )

        except Exception as e:
            self.logger.exception(f"Error publishing messages to SNS: {e}")
            raise
    
    @timing_decorator
    def batch_publish_messages(self, messages: list[B3StockTickerMessage]) -> None:
        """
        Publishes a batch of messages to the topic.

        Args:
            messages (list[B3StockTickerMessage]): A list of messages to publish (should be serializable).
        """
        
        # Preparing messages to be sent in batches
        try:
            entries = [
                {
                    "Id": str(uuid4()),
                    "Message": json.dumps(message.__dict__)
                }
                for message in messages
            ]
        except Exception as e:
            self.logger.error(f"Error preparing messages for batch publish into a SNS topic: {e}")
            raise

        # Sending messages in batches of 10 messages per batch
        topic_arn = self.__get_topic_arn()
        try:
            for i in range(0, len(entries), 10):
                batch_entries = entries[i:i + 10]

                _ = self.client.publish_batch(
                    TopicArn=topic_arn,
                    PublishBatchRequestEntries=batch_entries
                )

                # Logging the loop status
                log_loop_status(
                    logger=self.logger,
                    loop_idx=i // 10,
                    total_elements=len(messages) // 10,
                    log_pace=20,
                    log_msg=f"Published {i // 10} batches of 10 messages each to topic"
                )

        except Exception as e:
            self.logger.exception(f"Error publishing batch messages to SNS: {e}")
            raise
        else:
            self.logger.info(f"Successfully published messages to SNS topic {topic_arn}")
