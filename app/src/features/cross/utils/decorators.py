import os
import time
from functools import wraps

from app.src.features.cross.utils.log_utils import setup_logger


logger = setup_logger(__name__)


def timing_decorator(method=None, *, enabled=True):
    """
    Decorator to measure execution time of a method.
    
    Can be used with or without parentheses:
        @timing_decorator
        @timing_decorator(enabled=True)
    
    Args:
        enabled (bool): Whether timing is enabled.
    """
    def decorator(inner_method):
        @wraps(inner_method)
        def wrapper(self, *args, **kwargs):
            if enabled and logger:
                start_time = time.time()
                result = inner_method(self, *args, **kwargs)
                elapsed_time = time.time() - start_time

                class_name = self.__class__.__name__
                method_name = inner_method.__name__
                logger.info(f"{class_name}.{method_name} executed in {elapsed_time:.2f} seconds")
                
                return result

            else:
                return inner_method(self, *args, **kwargs)

        return wrapper

    # If method is None, this is being called with parentheses
    if method is None:
        return decorator
    else:
        return decorator(method)
