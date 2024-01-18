from category.models import CategoryModel
from .serializers import CategorySerializer

from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class CategoryListView(generics.ListAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # Get the serialized data using the serializer class
        serializer = self.get_serializer(self.get_queryset(), many=True)
        
        # Create a custom response dictionary with your desired key
        custom_response = {
            'data': serializer.data,
            'success':True, 
        }
        
        return Response(custom_response)
        