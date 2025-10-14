from dotenv import find_dotenv, load_dotenv

from app.src.features.get_active_stocks.presentation import get_active_stocks_presentation
from app.src.features.store_dynamodb_streams_data.presentation import store_dynamodb_streams_data_presentation
from app.src.features.get_fundamentus_eod_stock_metrics.presentation import get_fundamentus_eod_stock_metrics_presentation
from app.src.features.check_batch_processes_completion.presentation import check_batch_processes_completion_presentation
from app.src.features.send_batch_completion_emails.presentation import send_batch_completion_emails_presentation
from app.src.features.send_notification_emails.presentation import send_notification_emails_presentation
from app.tests.mocks.mocked_input_events import (
    MOCKED_DYNAMODB_STREAMS_EVENT_FOR_ACTIVE_STOCKS_TABLE,
    MOCKED_DYNAMODB_STREAMS_EVENT_FOR_BATCH_PROCESS_CONTROL_TABLE,
    MOCKED_SQS_EVENT_FOR_ACTIVE_STOCKS_QUEUE,
    MOCKED_SNS_EVENT_FOR_BATCH_COMPLETION_TOPIC,
    MOCKED_SNS_EVENT_NOTIFICATION_EMAIL_SUCCESS
)


# Loading environment variables from .env file
_ = load_dotenv(find_dotenv())

# Building handlers
get_active_stocks_handler = get_active_stocks_presentation.handler
store_dynamodb_streams_data_handler = store_dynamodb_streams_data_presentation.handler
get_fundamentus_eod_stock_metrics_handler = get_fundamentus_eod_stock_metrics_presentation.handler
check_batch_processes_completion_handler = check_batch_processes_completion_presentation.handler
send_batch_completion_emails_handler = send_batch_completion_emails_presentation.handler
send_notification_emails_handler = send_notification_emails_presentation.handler


"""
FEATURE: Get Active Stocks

DESCRIPTION:
    This feature provides functionality to scrape and retrieve active stock data from
    a web site (e.g., Fundamentus) and process it for further use.
"""
# response = get_active_stocks_handler(
#     event=None,
#     context=None
# )


"""
FEATURE: Store DynamoDB Streams Data

DESCRIPTION:
    This feature provides functionality to stream data from DynamoDB and process it in real-time.
"""
# response = store_dynamodb_streams_data_handler(
#   event=MOCKED_DYNAMODB_STREAMS_EVENT_FOR_ACTIVE_STOCKS_TABLE,
#   context=None
# )


"""
FEATURE: Get Fundamentus EOD Stock Metrics

DESCRIPTION:
    This feature provides functionality to scrape and retrieve end-of-day stock metrics from
    the Fundamentus investment website and process it for further use.
"""
# response = get_fundamentus_eod_stock_metrics_handler(
#     event=MOCKED_SQS_EVENT_FOR_ACTIVE_STOCKS_QUEUE,
#     context=None
# )


"""
FEATURE: Check Batch Processes Completion

DESCRIPTION:
    This feature provides functionality to receive stream data from a batch process control
    DynamoDB table and check the completion status of batch processes.
"""
# response = check_batch_processes_completion_handler(
#     event=MOCKED_DYNAMODB_STREAMS_EVENT_FOR_BATCH_PROCESS_CONTROL_TABLE,
#     context=None
# )


"""
FEATURE: Send Batch Completion Emails

DESCRIPTION:
    This feature provides functionality to send email notifications upon the completion of
    batch processes.
"""
# response = send_batch_completion_emails_handler(
#     event=MOCKED_SNS_EVENT_FOR_BATCH_COMPLETION_TOPIC,
#     context=None
# )


"""
FEATURE: Send Notification Emails

DESCRIPTION:
    This feature provides functionality to send email notifications upon specific events.
"""
response = send_notification_emails_handler(
    event=MOCKED_SNS_EVENT_NOTIFICATION_EMAIL_SUCCESS,
    context=None
)
