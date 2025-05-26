import pytest
from rest_framework.test import APIClient

from users.factories import UsersFactory
from users.models import Users


@pytest.mark.django_db
class TestUsersViewSet:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()

    def test_list_users(self):
        UsersFactory.create_batch(3)
        response = self.client.get("/api/users/")
        assert response.status_code == 200
        assert len(response.data) == 3

    def test_retrieve_user_detail(self):
        user = UsersFactory()
        response = self.client.get(f"/api/users/{user.id}/")
        assert response.status_code == 200
        assert response.data["id"] == user.id
        assert response.data["username"] == user.username

    def test_create_user(self):
        payload = {"username": "novousuario", "password": "senha123"}
        response = self.client.post("/api/users/", data=payload)
        assert response.status_code == 201
        assert Users.objects.filter(username="novousuario").exists()

    def test_get_me(self):
        user = UsersFactory(username="rafael", password="123")
        self.client.login(username="rafael", password="123")
        response = self.client.get("/api/users/me/")
        assert response.status_code == 200
        assert response.data["username"] == "rafael"
        assert response.data["id"] == user.id
