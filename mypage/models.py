from django.db import models
from django.contrib.auth import get_user_model
from app1.models import UploadFile

User = get_user_model()

class MyModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_file = models.ForeignKey(UploadFile, on_delete=models.CASCADE)
    # UploadFile 모델에서 분석 결과를 가져오는 메소드
    @property
    def analysis_score(self):
        return self.upload_file.analysis_score

    @property
    def analysis_phrase(self):
        return self.upload_file.analysis_phrase
