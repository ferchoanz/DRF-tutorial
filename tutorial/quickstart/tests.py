from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class QuickstartAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="quickstart-user",
            password="testpass123",
            email="quickstart@example.com",
        )
        self.group = Group.objects.create(name="Test Group")
        self.user.groups.add(self.group)

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_unauthenticated_user_list_is_rejected(self):
        self.client.credentials()
        url = reverse("user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_group_list_is_rejected(self):
        self.client.credentials()
        url = reverse("group-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_users_authenticated(self):
        url = reverse("user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["username"], self.user.username)

    def test_list_groups_authenticated(self):
        url = reverse("group-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], self.group.name)

    def test_retrieve_user(self):
        url = reverse("user-detail", args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)

    def test_retrieve_group(self):
        url = reverse("group-detail", args=[self.group.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.group.name)

    def test_create_user(self):
        url = reverse("user-list")
        payload = {
            "username": "new-user",
            "email": "new@example.com",
            "password": "newpass123",
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="new-user").exists())

    def test_create_group(self):
        url = reverse("group-list")
        payload = {"name": "New Group"}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Group.objects.filter(name="New Group").exists())

    def test_update_group(self):
        url = reverse("group-detail", args=[self.group.id])
        payload = {"name": "Updated Group"}
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.group.refresh_from_db()
        self.assertEqual(self.group.name, "Updated Group")

    def test_delete_group(self):
        url = reverse("group-detail", args=[self.group.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Group.objects.filter(id=self.group.id).exists())


class JWTAuthenticationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="jwt-user", password="jwtpass123"
        )

    def test_obtain_token_with_valid_credentials(self):
        url = reverse("token_obtain_pair")
        payload = {"username": "jwt-user", "password": "jwtpass123"}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_obtain_token_with_invalid_credentials(self):
        url = reverse("token_obtain_pair")
        payload = {"username": "jwt-user", "password": "wrongpassword"}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_protected_endpoint_with_valid_token(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        url = reverse("user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_protected_endpoint_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer invalid-token")
        url = reverse("user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
