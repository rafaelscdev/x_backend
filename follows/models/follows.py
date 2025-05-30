from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Follows(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="following", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="followers", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.follower.username} → {self.following.username}"

    def clean(self):
        if self.follower == self.following:
            raise ValidationError("Um usuário não pode seguir a si mesmo.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
