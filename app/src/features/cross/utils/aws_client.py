import boto3


class AWSClient:
    """
    A utility class for creating and managing AWS service clients using boto3.
    """

    @staticmethod
    def get_client(service_name: str, region_name: str = boto3.session.Session().region_name):
        """
        Get a boto3 client for the specified AWS service.

        Args:
            service_name (str): The name of the AWS service (e.g., 's3', 'ec2', 'sts').
            region_name (str, optional): The AWS region name. Defaults to the current session's region.
        
        Returns:
            boto3.client: A boto3 client for the specified service.
        """
        return boto3.client(service_name, region_name=region_name)


    @staticmethod
    def get_caller_account_id() -> str:
        """
        Get the AWS account ID of the caller.
        """
        sts_client = AWSClient.get_client(service_name="sts")
        return sts_client.get_caller_identity()['Account']


    @staticmethod
    def get_caller_region_name() -> str:
        """
        Get the AWS region name of the caller.
        """
        return boto3.session.Session().region_name
    

    @staticmethod
    def build_bucket_name_from_prefix(bucket_name_prefix: str) -> str:
        """
        Constructs the full S3 bucket name using the provided prefix and caller's account ID and region.

        Args:
            bucket_name_prefix (str): The prefix for the S3 bucket name.

        Returns:
            str: The full S3 bucket name.
        """
        account_id = AWSClient.get_caller_account_id()
        region_name = AWSClient.get_caller_region_name()
        return f"{bucket_name_prefix}-{account_id}-{region_name}"