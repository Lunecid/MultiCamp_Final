# models.py
# pip install pillow
from PIL import Image, ExifTags 
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
import os
from django.utils.timezone import now
# pip install django-resized
from django_resized import ResizedImageField
from django.conf import settings
from django.utils import timezone
import subprocess
import re
import logging




def upload_to(instance, filename):
    # 파일 확장자를 유지하면서 파일명을 현재 날짜와 시간으로 변경
    ext = filename.split('.')[-1]
    # 현재 날짜와 시간을 기반으로 파일 이름 설정
    filename = now().strftime('%Y_%m_%d_%H_%M')  # 마이크로초까지 포함하여 파일 이름의 고유성 확보
    # 파일 이름과 확장자를 결합
    filename = '{}.{}'.format(filename, ext)
    # 파일을 저장할 경로 반환 (예: 'images/2023_01_01_12_30.jpg')
    return os.path.join('images/upload', filename)

def rotate_image(uploaded_image):
    try:
        image = Image.open(uploaded_image)
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)

        output = BytesIO()
        image.save(output, format='JPEG', quality=75)
        output.seek(0)
        return InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % uploaded_image.name.split('.')[0], 'image/jpeg', output.tell(), None)
    except (AttributeError, KeyError, IndexError):
        # 이미지에 Exif 정보가 없는 경우 원본을 그대로 반환
        return uploaded_image

class UploadFile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    upload_date = models.DateTimeField( default=timezone.now)
    analysis_score = models.IntegerField(null=True, blank=True)  # 분석 점수 필드 추가
    analysis_phrase = models.CharField(max_length=255, null=True, blank=True)  # 분석 표현 필드 추가

    

    image = ResizedImageField(
        size=[640, 640],
        quality=75,
        upload_to=upload_to,
        force_format='JPEG'
    )

    def save(self, *args, **kwargs):
        if self.image:
            self.image = rotate_image(self.image)
        super(UploadFile, self).save(*args, **kwargs)
        
        # 이미지 저장 후 test.py 스크립트 실행
        script_path = os.path.join(os.getcwd(), 'MultiCamp_Final/app1/tests.py')
        process = subprocess.Popen(['python', script_path, self.image.path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
            
        # 분석 결과 파싱 (stdout 기반으로 적절한 파싱 로직 구현 필요)
        logger = logging.getLogger(__name__)
        analysis_result = stdout.decode().strip()
        logger.debug(f"Analysis result: {analysis_result}")

        
        # 예시: '제출한 사진을 분석한 결과 상태는 매우 적합이며, 15점을 획득하셨습니다.' 형태의 결과를 파싱
        # 파싱 로직을 여기에 구현...
        # parsed_score = ... # 파싱하여 얻은 점수
        # parsed_score = int(re.search(r'\b(\d+)\b점을 획득하셨습니다.', analysis_result).group(1))
        match = re.search(r'\b(\d+)\b점을 획득하셨습니다.', analysis_result)
        if match:
            self.analysis_score = int(match.group(1))  # 분석 결과 점수 저장
        else:
            logger.debug("No match found for score extraction.")
        
        super(UploadFile, self).save(*args, **kwargs)  # 부모 클래스의 save 메서드 호출 // 


        # 이미지 분석 점수를 바탕으로 TotalScore 업데이트
        total_score, created = TotalScore.objects.get_or_create(user=self.user)
        if self.analysis_score:
            total_score.total_score += self.analysis_score or 0
            total_score.save()
        

class TotalScore(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='total_score')
    total_score = models.IntegerField(default=0)  # 이미지 분석 점수의 총합

    def __str__(self):
        return f'{self.user.username}: {self.total_score}'
    
