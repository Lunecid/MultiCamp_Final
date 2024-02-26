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


class Score(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}: {self.points} points"

