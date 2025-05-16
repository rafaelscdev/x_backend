from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from posts.models import Post, Comment

User = get_user_model()

class PostTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post_data = {
            'content': 'Test post content'
        }
        self.post = Post.objects.create(user=self.user, **self.post_data)

    def test_create_post(self):
        """Teste de criação de post básico"""
        self.assertEqual(self.post.user, self.user)
        self.assertEqual(self.post.content, self.post_data['content'])
        self.assertIsNotNone(self.post.created_at)

    def test_post_str(self):
        """Teste de representação string do post"""
        expected = f'Post de {self.user.username}'
        self.assertEqual(str(self.post), expected)

class PostAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.post_data = {
            'content': 'Test post content'
        }
        self.post = Post.objects.create(user=self.user, **self.post_data)

    def test_create_post_api(self):
        """Teste de criação de post via API"""
        response = self.client.post('/api/posts/', self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        post = Post.objects.latest('created_at')
        self.assertEqual(post.content, self.post_data['content'])
        self.assertEqual(post.user, self.user)

    def test_like_post(self):
        """Teste de like em post"""
        response = self.client.post(f'/api/posts/{self.post.id}/like/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.likes.count(), 1)
        self.assertTrue(self.post.likes.filter(id=self.user.id).exists())

    def test_comment_post(self):
        """Teste de comentário em post"""
        comment_data = {'content': 'Test comment'}
        response = self.client.post(
            f'/api/posts/{self.post.id}/comments/',
            comment_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.content, comment_data['content'])
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.post, self.post)

    def test_delete_own_post(self):
        """Teste de deleção do próprio post"""
        response = self.client.delete(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_cannot_delete_others_post(self):
        """Teste de tentativa de deleção de post de outro usuário"""
        other_post = Post.objects.create(user=self.other_user, content='Other post')
        response = self.client.delete(f'/api/posts/{other_post.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 2)

    def test_post_ordering(self):
        """Teste de ordenação dos posts"""
        # Limpar posts existentes
        Post.objects.all().delete()
        
        # Criar primeiro post
        self.client.post('/api/posts/', {'content': 'Primeiro post'})
        
        # Criar segundo post
        response = self.client.post('/api/posts/', {'content': 'Segundo post!'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Buscar posts via API
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar ordenação
        posts = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0]['content'], 'Segundo post!')  # Mais recente primeiro
        self.assertEqual(posts[1]['content'], 'Primeiro post')  # Post mais antigo por último 