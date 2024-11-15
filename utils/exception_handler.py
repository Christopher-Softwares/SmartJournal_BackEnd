from rest_framework.views import exception_handler
from rest_framework import status
from .response_wrapper import standard_response

def standard_exception_handler(exc, context):
    response = exception_handler(exc, context) # REST framework's default exception handler

    if response is not None:
        # Project standard format
        return standard_response(
            data=None,
            errors=response.data,
            is_success=False,
            status_code=response.status_code,
        )
    else:
        
        print(str(exc))
        
        # internal server error
        return standard_response(
            data=None,
            errors={"detail": "An unexpected error occurred"},
            is_success=False,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
