from django.db import models
from django.contrib.auth import get_user_model
from app1.models import UploadFile

User = get_user_model()

class MyModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_file = models.ForeignKey(UploadFile, on_delete=models.CASCADE)

    # 다른 필드들을 필요에 따라 추가할 수 있습니다.
