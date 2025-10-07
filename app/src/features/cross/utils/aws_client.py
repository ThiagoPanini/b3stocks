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