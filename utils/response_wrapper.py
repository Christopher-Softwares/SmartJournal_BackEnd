from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

#RESPONSE WRAPPER
def standard_response(data=None, errors=None, is_success=True, status_code=200):
    """
    A utility function to standardize the API response format.
    
    :param data: The response data if the operation is successful
    :param errors: The error details if the operation fails
    :param is_success: Boolean indicating if the operation was successful
    :param status_code: HTTP status code of the response
    :return: A DRF Response object with a standardized structure
    """
    
    response_structure = {
        "data": data if is_success is True else [],
        "errors": errors if is_success is False else [],
        "is_success": is_success,
        "status_code": status_code
    }
    
    return Response(response_structure, status=status_code)


# STANDARDIZED VIEWS
class StandardAPIView(generics.GenericAPIView):
    """
    Custom API View that returns responses in a standardized format.
    """

    def create_response(self, data=None, errors=None, is_success=True, status_code=status.HTTP_200_OK):
        return standard_response(data, errors, is_success, status_code)


class StandardListAPIView(StandardAPIView, generics.ListAPIView):
    """
    Custom List API View that returns resposnes in a standardized format.
    """
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset=queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.create_response(data=serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return self.create_response(data=serializer.data)


class StandardRetrieveAPIView(StandardAPIView, generics.RetrieveAPIView):
    """
    Custom Retrieve API View that returns responses in a standardized format.
    """

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.create_response(data=serializer.data)


class StandardCreateAPIView(StandardAPIView, generics.CreateAPIView):
    """
    Custom Create API View that returns responses in a standardized format.
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self.create_response(data=serializer.data, status_code=status.HTTP_201_CREATED)


class StandardUpdateAPIView(StandardAPIView, generics.UpdateAPIView):
    """
    Custom Update API View that returns responses in a standardized format.
    """

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return self.create_response(data=serializer.data)


class StandardDestroyAPIView(StandardAPIView, generics.DestroyAPIView):
    """
    Custom Destroy API View that returns responses in a standardized format.
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return self.create_response(status_code=status.HTTP_204_NO_CONTENT)
