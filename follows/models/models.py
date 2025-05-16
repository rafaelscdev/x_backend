from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='following',
        on_delete=models.CASCADE
    )
    followed = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='followers',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.follower.username} → {self.followed.username}'

    def clean(self):
        if self.follower == self.followed:
            raise ValidationError('Um usuário não pode seguir a si mesmo.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs) 