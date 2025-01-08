from rest_framework import status
from django.shortcuts import get_object_or_404
from .api_response import api_response

class CRUDMixin:
    model = None
    serializer_class = None
    lookup_field = 'id'

    def get_object(self, pk):
        return get_object_or_404(self.model, **{self.lookup_field: pk})

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(serializer.data, status_code=status.HTTP_201_CREATED)
        return api_response(error=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        name_query = request.query_params.get('name', '')
        if name_query:
            objects = self.model.objects.filter(name__icontains=name_query)
        else:
            objects = self.model.objects.all()
        serializer = self.serializer_class(objects, many=True)
        return api_response(serializer.data)

    def retrieve_update_delete(self, request, pk):
        instance = self.get_object(pk)
        
        if request.method == 'GET':
            serializer = self.serializer_class(instance)
            return api_response(serializer.data)
            
        elif request.method == 'PUT':
            serializer = self.serializer_class(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return api_response(serializer.data)
            return api_response(error=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
            
        elif request.method == 'DELETE':
            instance.delete()
            return api_response(status_code=status.HTTP_204_NO_CONTENT)
