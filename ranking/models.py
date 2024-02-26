from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser




class UserScore(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ranking_score')
    points = models.IntegerField(default=0)

    class Meta:
        ordering = ['-points']

    def __str__(self):
        return f"{self.user.username}: {self.points}"
# 사용자 모델

class User(AbstractUser):
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)  # 사용자 사진
