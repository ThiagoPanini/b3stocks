import traceback
import inspect
import hashlib
import os
from datetime import datetime
from typing import Dict, Any, Optional, Type
from ..domain.entities.exception_info import ExceptionInfo, ExceptionCategory


class ExceptionUtils:
    """
    Utility class for extracting comprehensive information from exceptions.
    """
    
    # Mapping of exception types to categories
    EXCEPTION_CATEGORY_MAP = {
        'ConnectionError': ExceptionCategory.NETWORK,
        'TimeoutError': ExceptionCategory.TIMEOUT,
        'HTTPError': ExceptionCategory.NETWORK,
        'URLError': ExceptionCategory.NETWORK,
        'TypeError': ExceptionCategory.VALIDATION,
        'ValueError': ExceptionCategory.VALIDATION,
        'KeyError': ExceptionCategory.VALIDATION,
        'IndexError': ExceptionCategory.VALIDATION,
        'AttributeError': ExceptionCategory.DATA_PROCESSING,
        'FileNotFoundError': ExceptionCategory.RESOURCE,
        'PermissionError': ExceptionCategory.AUTHENTICATION,
        'MemoryError': ExceptionCategory.RESOURCE,
        'OSError': ExceptionCategory.SYSTEM,
        'RuntimeError': ExceptionCategory.SYSTEM,
    }
    
    @staticmethod
    def extract_exception_info(
        exception: Exception,
        feature_name: Optional[str] = None,
        environment: Optional[str] = None,
        process_version: Optional[str] = None,
        additional_context: Optional[Dict[str, Any]] = None
    ) -> ExceptionInfo:
        """
        Extract comprehensive information from an exception.
        
        Args:
            exception: The exception to analyze
            feature_name: Name of the feature/process where exception occurred
            environment: Runtime environment (dev, staging, prod)
            process_version: Version of the process/application
            additional_context: Additional context information
        
        Returns:
            ExceptionInfo object with extracted information
        """
        # Get exception basic info
        exc_type = type(exception).__name__
        exc_message = str(exception)
        
        # Extract stack trace information
        tb = exception.__traceback__
        stack_trace = traceback.format_exception(type(exception), exception, tb)
        stack_trace_str = ''.join(stack_trace)
        
        # Get the frame where exception occurred
        frame_info = ExceptionUtils._get_exception_frame_info(tb)
        
        # Extract local variables (sanitized)
        local_vars = ExceptionUtils._extract_local_variables(tb)
        
        # Generate fingerprint for deduplication
        fingerprint = ExceptionUtils._generate_fingerprint(
            exc_type, exc_message, frame_info['module'], frame_info['function'], frame_info['line']
        )
        
        # Determine category
        category = ExceptionUtils.EXCEPTION_CATEGORY_MAP.get(exc_type, ExceptionCategory.UNKNOWN)
        
        # Generate error code
        error_code = f"{exc_type}_{frame_info['line']}_{fingerprint[:8]}"
        
        return ExceptionInfo(
            exception_type=exc_type,
            exception_message=exc_message,
            exception_module=frame_info['module'],
            exception_function=frame_info['function'],
            exception_line=frame_info['line'],
            occurred_at=datetime.utcnow(),
            category=category,
            stack_trace=stack_trace_str,
            local_variables=local_vars,
            feature_name=feature_name,
            environment=environment or os.getenv('ENVIRONMENT', 'unknown'),
            process_version=process_version,
            error_code=error_code,
            fingerprint=fingerprint,
            additional_context=additional_context or {}
        )
    
    @staticmethod
    def _get_exception_frame_info(tb) -> Dict[str, Any]:
        """Extract information from the traceback frame where exception occurred."""
        if not tb:
            return {
                'module': 'unknown',
                'function': 'unknown',
                'line': 0,
                'filename': 'unknown'
            }
        
        # Get the last frame (where exception occurred)
        while tb.tb_next:
            tb = tb.tb_next
        
        frame = tb.tb_frame
        filename = frame.f_code.co_filename
        function_name = frame.f_code.co_name
        line_number = tb.tb_lineno
        
        # Extract module name from filename
        module_name = os.path.splitext(os.path.basename(filename))[0]
        
        return {
            'module': module_name,
            'function': function_name,
            'line': line_number,
            'filename': filename
        }
    
    @staticmethod
    def _extract_local_variables(tb, max_vars: int = 10) -> Dict[str, Any]:
        """
        Extract local variables from the exception frame (sanitized).
        """
        if not tb:
            return {}
        
        # Get the last frame
        while tb.tb_next:
            tb = tb.tb_next
        
        frame = tb.tb_frame
        local_vars = {}
        
        # Get local variables, excluding sensitive ones
        sensitive_keys = {'password', 'token', 'key', 'secret', 'auth', 'credential'}
        
        count = 0
        for var_name, var_value in frame.f_locals.items():
            if count >= max_vars:
                break
                
            # Skip sensitive variables
            if any(sensitive in var_name.lower() for sensitive in sensitive_keys):
                local_vars[var_name] = '[REDACTED]'
            else:
                # Safely convert to string
                try:
                    if isinstance(var_value, (str, int, float, bool, type(None))):
                        local_vars[var_name] = str(var_value)
                    else:
                        local_vars[var_name] = f"<{type(var_value).__name__}>"
                except:
                    local_vars[var_name] = '<unable_to_serialize>'
            
            count += 1
        
        return local_vars
    
    @staticmethod
    def _generate_fingerprint(exc_type: str, exc_message: str, module: str, function: str, line: int) -> str:
        """Generate a unique fingerprint for exception deduplication."""
        # Create a hash based on exception characteristics
        fingerprint_data = f"{exc_type}:{module}:{function}:{line}:{exc_message[:100]}"
        return hashlib.md5(fingerprint_data.encode()).hexdigest()
    
    @staticmethod
    def create_mock_exception_info(
        exception_type: str = "TypeError",
        feature_name: str = "Stock Data Processor"
    ) -> ExceptionInfo:
        """
        Create a mock exception info for testing purposes.
        """
        mock_exceptions = {
            "TypeError": {
                "message": "unsupported operand type(s) for +: 'NoneType' and 'str'",
                "module": "stock_processor",
                "function": "process_stock_data",
                "line": 127,
                "category": ExceptionCategory.VALIDATION
            },
            "ConnectionError": {
                "message": "HTTPSConnectionPool(host='fundamentus.com.br', port=443): Max retries exceeded",
                "module": "data_fetcher",
                "function": "fetch_stock_data",
                "line": 89,
                "category": ExceptionCategory.NETWORK
            },
            "ValueError": {
                "message": "invalid literal for int() with base 10: 'N/A'",
                "module": "data_validator",
                "function": "validate_financial_metrics",
                "line": 203,
                "category": ExceptionCategory.VALIDATION
            }
        }
        
        mock_data = mock_exceptions.get(exception_type, mock_exceptions["TypeError"])
        
        return ExceptionInfo(
            exception_type=exception_type,
            exception_message=mock_data["message"],
            exception_module=mock_data["module"],
            exception_function=mock_data["function"],
            exception_line=mock_data["line"],
            occurred_at=datetime.utcnow(),
            category=mock_data["category"],
            stack_trace=f"Traceback (most recent call last):\n  File \"{mock_data['module']}.py\", line {mock_data['line']}, in {mock_data['function']}\n{exception_type}: {mock_data['message']}",
            feature_name=feature_name,
            environment="staging",
            process_version="v2.1.0",
            error_code=f"{exception_type}_{mock_data['line']}_abc12345",
            fingerprint="abc12345def67890",
            retry_count=3,
            additional_context={
                "batch_size": 50,
                "processed_symbols": 23,
                "failed_at_symbol": "PETR4"
            }
        )