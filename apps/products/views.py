# from django.shortcuts import render
from rest_framework import viewsets

# from rest_framework.response import Response
# from rest_framework.request import Request
# import json
# from django.forms.models import model_to_dict

from .models import Product
from .serializers import ProductSerializer

# jwt authentication
from rest_framework.permissions import IsAuthenticated


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(active=True).order_by("-created_at")
    serializer_class = ProductSerializer
    
    # jwt authentication
    permission_classes = [IsAuthenticated]

    # def list(self, request: Request) -> Response:
    #     return Response({"method": request.method})
    #     json_user = model_to_dict(
    #         request.user,
    #         exclude=[
    #             "password",
    #             "last_login",
    #             "is_superuser",
    #             "is_staff",
    #             "is_active",
    #             "date_joined",
    #         ],
    #     )
    #     print(f"Auth: {json.dumps(request.auth.__dict__, default=str)}")
    #     print(f"User: {json_user}")
    #     return Response({"user": json_user})
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
