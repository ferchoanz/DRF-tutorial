from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet  # Asegúrate de importar tu ViewSet

# Instanciamos el router
router = DefaultRouter(trailing_slash=False)

# Registramos el endpoint 'products' mapeado al ProductViewSet
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]