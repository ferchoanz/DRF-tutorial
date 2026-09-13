# from django.shortcuts import render
from rest_framework import viewsets

# from rest_framework.response import Response
# from rest_framework.request import Request
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(active=True).order_by("-created_at")
    serializer_class = ProductSerializer

    # def list(self, request: Request) -> Response:
    #     return Response({"message": request.method})
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
