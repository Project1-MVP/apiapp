from functools import wraps
from django.db import transaction
from .api_response import api_response
from rest_framework import status

def atomic_transaction():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with transaction.atomic():
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    transaction.set_rollback(True)
                    return api_response(error=f"Transaction failed: {str(e)}", 
                                     status_code=status.HTTP_400_BAD_REQUEST)
        return wrapper
    return decorator
