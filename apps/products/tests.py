from decimal import Decimal

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.products.models import Product


class ProductAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        self.product = Product.objects.create(
            name="Test Product",
            price=Decimal("19.99"),
            description="A product for tests",
            active=True,
        )
        self.inactive_product = Product.objects.create(
            name="Inactive Product",
            price=Decimal("9.99"),
            description="Should not appear in list",
            active=False,
        )

    def test_unauthenticated_requests_are_rejected(self):
        self.client.credentials()
        url = reverse("product-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_products_returns_only_active_items(self):
        url = reverse("product-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], self.product.name)

    def test_create_product(self):
        url = reverse("product-list")
        payload = {
            "name": "New Product",
            "price": "29.99",
            "description": "New description",
            "active": True,
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 3)
        self.assertEqual(response.data["name"], payload["name"])

    def test_create_product_invalid_price(self):
        url = reverse("product-list")
        payload = {
            "name": "Bad Product",
            "price": "not-a-number",
            "description": "",
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_product(self):
        url = reverse("product-detail", args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product.name)
        self.assertEqual(response.data["price"], "19.99")

    def test_update_product(self):
        url = reverse("product-detail", args=[self.product.id])
        payload = {
            "name": "Updated Product",
            "price": "39.99",
            "description": "Updated description",
            "active": True,
        }
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, payload["name"])
        self.assertEqual(str(self.product.price), payload["price"])

    def test_partial_update_product(self):
        url = reverse("product-detail", args=[self.product.id])
        payload = {"name": "Partially Updated"}
        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, payload["name"])

    def test_delete_product(self):
        url = reverse("product-detail", args=[self.product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.filter(active=True).count(), 0)

    def test_pagination_is_applied(self):
        for i in range(15):
            Product.objects.create(
                name=f"Product {i}",
                price=Decimal("10.00"),
                active=True,
            )
        url = reverse("product-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 16)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertIsNotNone(response.data["next"])
