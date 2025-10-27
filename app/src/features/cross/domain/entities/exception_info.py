from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
import uuid


@dataclass
class ExceptionInfo:
    """
    Comprehensive exception information entity for standardized error handling.

    Attributes:
        exception_type (str): The type of the exception (e.g., ValueError, TypeError).
        exception_message (str): The message associated with the exception.
        exception_module (str): The module where the exception occurred.
        exception_function (str): The function where the exception occurred.
        exception_line (int): The line number where the exception occurred.
        error_code (Optional[str]): An optional error code for categorizing the exception.
        stack_trace (Optional[str]): The stack trace of the exception for debugging.
        root_cause_hint (Optional[str]): A hint to help identify the root cause of the exception.
    """
    exception_type: str
    exception_message: str
    exception_module: str
    exception_function: str
    exception_line: int
    error_code: Optional[str] = None
    stack_trace: Optional[str] = None
    root_cause_hint: Optional[str] = None


    def __post_init__(self):
        self.root_cause_hint = self._generate_root_cause_hint()


    def to_template_dict(self) -> Dict[str, str]:
        """
        Convert exception info to template-friendly dictionary for HTML templates.
        """
        return {
            'error_message': self.exception_message,
            'error_code': self.error_code or f"{self.exception_type}_{self.exception_line}",
            'root_cause_hint': self._generate_root_cause_hint(),
            'first_failure_time': self.occurred_at.strftime('%Y-%m-%d %H:%M:%S UTC'),
            'last_attempt_time': self.occurred_at.strftime('%Y-%m-%d %H:%M:%S UTC'),
            'retry_attempts': str(self.retry_count),
            'next_retry_time': 'Manual intervention required',
            'process_id': self.process_id,
            'trace_id': self.fingerprint or self.process_id[:8],
            'exception_type': self.exception_type,
            'exception_location': f"{self.exception_module}.{self.exception_function}:{self.exception_line}",
            'category': self.category.value,
        }
    
    def _generate_root_cause_hint(self) -> str:
        """Generate a human-readable root cause hint based on exception details."""
        hints = {
            'TypeError': 'Data type mismatch or incorrect argument types',
            'ValueError': 'Invalid data values or format issues',
            'KeyError': 'Missing required data fields or configuration',
            'ConnectionError': 'Network connectivity or service availability issues',
            'TimeoutError': 'Service response time exceeded threshold',
            'FileNotFoundError': 'Missing required files or incorrect file paths',
            'PermissionError': 'Insufficient access rights or authentication issues',
            'AttributeError': 'Object method/property access issues or API changes',
        }
        
        return hints.get(self.exception_type, 'Unknown error type - requires investigation')
