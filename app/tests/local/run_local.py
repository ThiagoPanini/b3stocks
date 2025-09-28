from dotenv import find_dotenv, load_dotenv

from app.src.features.get_active_stocks.presentation import get_active_stocks_presentation
from app.src.features.store_dynamodb_streams_data.presentation import store_dynamodb_streams_data_presentation
from app.src.features.get_fundamentus_eod_stock_metrics.presentation import get_fundamentus_eod_stock_metrics_presentation
from app.src.features.check_batch_processes_completion.presentation import check_batch_processes_completion_presentation

from app.tests.mocks.mocked_input_events import (
    MOCKED_DYNAMODB_STREAMS_EVENT_FOR_ACTIVE_STOCKS_TABLE,
    MOCKED_DYNAMODB_STREAMS_EVENT_FOR_BATCH_PROCESS_CONTROL_TABLE,
    MOCKED_SQS_EVENT_FOR_ACTIVE_STOCKS_QUEUE
)


# Loading environment variables from .env file
_ = load_dotenv(find_dotenv())

# Building handlers
get_active_stocks_handler = get_active_stocks_presentation.handler
store_dynamodb_streams_data_handler = store_dynamodb_streams_data_presentation.handler
get_fundamentus_eod_stock_metrics_handler = get_fundamentus_eod_stock_metrics_presentation.handler
check_batch_processes_completion_handler = check_batch_processes_completion_presentation.handler


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


import boto3
import json
from datetime import datetime
from typing import Dict, Any
from botocore.exceptions import ClientError


class HTMLEmailSender:
    """
    A simple class to handle HTML email sending with S3 templates.
    """
    
    def __init__(self, region_name: str = 'us-east-1'):
        """
        Initialize the email sender with AWS clients.
        
        Args:
            region_name (str): AWS region name
        """
        self.s3_client = boto3.client('s3', region_name=region_name)
        self.ses_client = boto3.client('ses', region_name=region_name)
        self.region_name = region_name
    
    def get_html_template_from_s3(self, bucket_name: str, template_key: str) -> str:
        """
        Retrieve HTML template from S3 bucket.
        
        Args:
            bucket_name (str): S3 bucket name
            template_key (str): S3 object key for the HTML template
            
        Returns:
            str: HTML template content
            
        Raises:
            Exception: If template cannot be retrieved from S3
        """
        try:
            print(f"Retrieving HTML template from s3://{bucket_name}/{template_key}")
            
            response = self.s3_client.get_object(Bucket=bucket_name, Key=template_key)
            html_content = response['Body'].read().decode('utf-8')
            
            print("✅ HTML template retrieved successfully")
            return html_content
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchBucket':
                raise Exception(f"S3 bucket '{bucket_name}' does not exist")
            elif error_code == 'NoSuchKey':
                raise Exception(f"Template '{template_key}' not found in bucket '{bucket_name}'")
            else:
                raise Exception(f"Error retrieving template: {e}")
    
    def replace_template_placeholders(self, html_template: str, data: Dict[str, Any]) -> str:
        """
        Replace placeholders in HTML template with actual data.
        
        Args:
            html_template (str): HTML template with placeholders like {{placeholder_name}}
            data (Dict[str, Any]): Dictionary with placeholder names and values
            
        Returns:
            str: HTML content with replaced placeholders
        """
        print("🔄 Replacing template placeholders...")
        
        html_content = html_template
        
        for placeholder, value in data.items():
            placeholder_pattern = f"{{{{{placeholder}}}}}"
            html_content = html_content.replace(placeholder_pattern, str(value))
            print(f"   Replaced {{{{ {placeholder} }}}} with: {value}")
        
        print("✅ Template placeholders replaced successfully")
        return html_content
    
    def send_html_email(
        self, 
        from_email: str, 
        to_emails: list, 
        subject: str, 
        html_body: str,
        text_body: str = None
    ) -> Dict[str, Any]:
        """
        Send HTML email using AWS SES.
        
        Args:
            from_email (str): Sender email address (must be verified in SES)
            to_emails (list): List of recipient email addresses
            subject (str): Email subject
            html_body (str): HTML email body
            text_body (str, optional): Plain text email body
            
        Returns:
            Dict[str, Any]: SES response
            
        Raises:
            Exception: If email cannot be sent
        """
        try:
            print(f"📧 Sending email to: {', '.join(to_emails)}")
            print(f"   Subject: {subject}")
            
            # Prepare email body
            body = {'Html': {'Data': html_body, 'Charset': 'UTF-8'}}
            
            if text_body:
                body['Text'] = {'Data': text_body, 'Charset': 'UTF-8'}
            
            # Send email
            response = self.ses_client.send_email(
                Source=from_email,
                Destination={'ToAddresses': to_emails},
                Message={
                    'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                    'Body': body
                },
                # Optional: Use configuration set for tracking
                # ConfigurationSetName='b3stocks-email-config'
            )
            
            message_id = response['MessageId']
            print(f"✅ Email sent successfully! Message ID: {message_id}")
            
            return response
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            
            if error_code == 'MessageRejected':
                raise Exception("Email was rejected by SES. Check recipient addresses and content.")
            elif error_code == 'MailFromDomainNotVerifiedException':
                raise Exception(f"Sender email '{from_email}' is not verified in SES")
            elif error_code == 'ConfigurationSetDoesNotExistException':
                raise Exception("SES configuration set does not exist")
            else:
                raise Exception(f"Error sending email: {e}")
    
    def send_batch_completion_notification(
        self,
        bucket_name: str,
        template_key: str,
        from_email: str,
        to_emails: list,
        batch_process_name: str,
        completion_status: str,
        execution_date: str,
        total_records: int = None,
        execution_time: str = None,
        additional_info: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Send a batch process completion notification email.
        
        Args:
            bucket_name (str): S3 bucket containing the HTML template
            template_key (str): S3 key for the HTML template
            from_email (str): Sender email address
            to_emails (list): List of recipient email addresses
            batch_process_name (str): Name of the batch process
            completion_status (str): Status of completion (SUCCESS, FAILED, etc.)
            execution_date (str): Date when the process was executed
            total_records (int, optional): Number of records processed
            execution_time (str, optional): Time taken for execution
            additional_info (Dict[str, Any], optional): Additional information to include
            
        Returns:
            Dict[str, Any]: SES response
        """
        print(f"🚀 Starting batch completion notification for: {batch_process_name}")
        
        # Get HTML template from S3
        html_template = self.get_html_template_from_s3(bucket_name, template_key)
        
        # Prepare template data
        template_data = {
            'batch_process_name': batch_process_name,
            'completion_status': completion_status,
            'execution_date': execution_date,
            'current_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
            'total_records': total_records or 'N/A',
            'execution_time': execution_time or 'N/A'
        }
        
        # Add additional info if provided
        if additional_info:
            template_data.update(additional_info)
        
        # Replace placeholders in template
        html_content = self.replace_template_placeholders(html_template, template_data)

        # Write html content locally to further analysis if needed
        with open('last_sent_email.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Prepare email subject
        status_emoji = "✅" if completion_status.upper() == "SUCCESS" else "❌"
        subject = f"{status_emoji} B3Stocks - {batch_process_name} - {completion_status}"
        
        # Send email
        return self.send_html_email(
            from_email=from_email,
            to_emails=to_emails,
            subject=subject,
            html_body=html_content
        )


def create_sample_html_template() -> str:
    """
    Create a sample HTML template for testing purposes.
    
    Returns:
        str: Sample HTML template content
    """
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>B3Stocks - Batch Process Notification</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 8px 8px 0 0;
        }
        .content {
            background-color: #f8f9fa;
            padding: 30px;
            border-radius: 0 0 8px 8px;
            border: 1px solid #dee2e6;
        }
        .status-success {
            color: #28a745;
            font-weight: bold;
        }
        .status-failed {
            color: #dc3545;
            font-weight: bold;
        }
        .info-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        .info-table th,
        .info-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #dee2e6;
        }
        .info-table th {
            background-color: #e9ecef;
            font-weight: bold;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            padding: 20px;
            font-size: 12px;
            color: #6c757d;
        }
        .logo {
            max-width: 200px;
            height: auto;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏦 B3Stocks</h1>
        <h2>Batch Process Notification</h2>
    </div>
    
    <div class="content">
        <h3>Process: {{batch_process_name}}</h3>
        
        <p>
            Status: 
            <span class="status-{{completion_status}}">
                {{completion_status}}
            </span>
        </p>
        
        <table class="info-table">
            <tr>
                <th>Execution Date</th>
                <td>{{execution_date}}</td>
            </tr>
            <tr>
                <th>Notification Time</th>
                <td>{{current_timestamp}}</td>
            </tr>
            <tr>
                <th>Total Records Processed</th>
                <td>{{total_records}}</td>
            </tr>
            <tr>
                <th>Execution Time</th>
                <td>{{execution_time}}</td>
            </tr>
        </table>
        
        <p><strong>Additional Information:</strong></p>
        <ul>
            <li>This notification was automatically generated by the B3Stocks system</li>
            <li>Process execution completed at {{current_timestamp}}</li>
            <li>For technical support, please contact the development team</li>
        </ul>
        
        <p>
            <em>
                Thank you for using B3Stocks! 
                This system helps you track and analyze Brazilian stock market data.
            </em>
        </p>
    </div>
    
    <div class="footer">
        <p>© 2025 B3Stocks - Brazilian Stock Market Analytics</p>
        <p>This is an automated message. Please do not reply to this email.</p>
    </div>
</body>
</html>
"""


def main():
    """
    Main function to demonstrate the HTML email functionality.
    """
    print("🔧 B3Stocks HTML Email Sender - Sample Script")
    print("=" * 50)
    
    # Configuration (you need to update these values)
    CONFIG = {
        'region_name': 'sa-east-1',  # Update with your AWS region
        'bucket_name': 'b3stocks-artifacts-596533897380-sa-east-1',  # Update with your S3 bucket
        'template_key': 'mail-templates/batch-completion-template.html',  # Template path in S3
        'from_email': 'panini.development@gmail.com',  # Must be verified in SES (use same as to_emails for testing)
        'to_emails': ['panini.development@gmail.com'],  # Update with recipient emails (must be verified in SES sandbox)
        'ses_configuration_set': 'b3stocks-email-config',  # SES configuration set from Terraform
    }
    
    try:
        # Initialize email sender
        email_sender = HTMLEmailSender(region_name=CONFIG['region_name'])
        
        # Example: Send batch completion notification
        print("\n📧 Sending batch completion notification...")
        
        response = email_sender.send_batch_completion_notification(
            bucket_name=CONFIG['bucket_name'],
            template_key=CONFIG['template_key'],
            from_email=CONFIG['from_email'],
            to_emails=CONFIG['to_emails'],
            batch_process_name='Get Fundamentus EOD Stock Metrics',
            completion_status='SUCCESS',
            execution_date='2025-09-28',
            total_records=1234,
            execution_time='2 minutes 30 seconds',
            additional_info={
                'region': CONFIG['region_name'],
                'environment': 'production'
            }
        )
        
        print(f"\n🎉 Email sent successfully!")
        print(f"   Message ID: {response['MessageId']}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Make sure to:")
        print("   1. Update the CONFIG dictionary with your actual values")
        print("   2. Verify your sender email in AWS SES")
        print("   3. Create the HTML template in your S3 bucket")
        print("   4. Configure AWS credentials (AWS CLI, IAM role, etc.)")


def create_sample_template_file():
    """
    Helper function to create a sample HTML template file locally.
    You can upload this file to your S3 bucket for testing.
    """
    template_content = create_sample_html_template()
    
    with open('batch-completion-template.html', 'w', encoding='utf-8') as f:
        f.write(template_content)
    
    print("📄 Sample HTML template created: batch-completion-template.html")
    print("   Upload this file to your S3 bucket for testing")


if __name__ == "__main__":
    # Uncomment the line below to create a sample template file
    create_sample_template_file()
    
    # Run the main email sending demonstration
    main()