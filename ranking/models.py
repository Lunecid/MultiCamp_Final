from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class UserScore(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ranking_score')
    points = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)

    class Meta:
        ordering = ['-points']

    def save(self, *args, **kwargs):
        if not self.id:
            # 새로운 객체일 경우에만 순위 계산
            max_rank = UserScore.objects.aggregate(models.Max('rank'))['rank__max'] or 0
            self.rank = max_rank + 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}: {self.points}, Rank: {self.rank}"

# 사용자 모델
class User(AbstractUser):
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)
