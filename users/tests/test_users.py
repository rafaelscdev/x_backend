from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

User = get_user_model()

class UserTests(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_create_user(self):
        """Teste de criação de usuário básico"""
        self.assertEqual(self.user.username, self.user_data['username'])
        self.assertEqual(self.user.email, self.user_data['email'])
        self.assertTrue(self.user.check_password(self.user_data['password']))

    def test_email_unique(self):
        """Teste de unicidade do email"""
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='another',
                email=self.user_data['email'],
                password='another123'
            )

class UserAPITests(APITestCase):
    def setUp(self):
        self.register_url = '/api/users/register/'
        self.login_url = '/api/users/token/'
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password2': 'testpass123'  # Campo necessário para confirmação
        }

    def test_create_user_api(self):
        """Teste de criação de usuário via API"""
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get()
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.email, self.user_data['email'])

    def test_login_user(self):
        """Teste de login de usuário"""
        # Criar usuário primeiro
        user_data = {
            'username': self.user_data['username'],
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        User.objects.create_user(**user_data)
        
        # Tentar login
        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_update_profile(self):
        """Teste de atualização de perfil"""
        user_data = {
            'username': self.user_data['username'],
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        user = User.objects.create_user(**user_data)
        self.client.force_authenticate(user=user)
        
        update_data = {
            'bio': 'Nova bio',
            'email': 'newemail@example.com'
        }
        
        response = self.client.patch('/api/users/me/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.bio, update_data['bio'])
        self.assertEqual(user.email, update_data['email']) 