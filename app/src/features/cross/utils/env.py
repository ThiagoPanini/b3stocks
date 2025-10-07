import os

class EnvironmentVarsUtils:

    @staticmethod
    def check_required_env_vars(required_env_vars: list[str]) -> None:
        """
        Checks if all required environment variables are present.

        Args:
            required_vars (list[str]): List of required environment variable names.
        
        Raises:
            EnvironmentError: If any required environment variable is missing.
        """
        missing_vars = [var for var in required_env_vars if var not in os.environ]
        if missing_vars:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")
