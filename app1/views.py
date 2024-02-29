from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import UploadFile,Score
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
import os
import torch

def main(request):
    return render(request, 'main.html')


# Create your views here.
@login_required(login_url='accounts:login')
def index(request):
    return render(request, 'index.html')

@login_required(login_url='accounts:login')
def image_upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # image = form.cleaned_data['image']
            # new_file = UploadFile(image=image)
            # new_file.save()

            upload_file = form.save(commit=False)
            upload_file.user = request.user  # 현재 로그인한 사용자를 user 필드에 할당
            upload_file.save()


              # 이미지 파일 시스템 경로 생성
            img_path = os.path.join(settings.MEDIA_ROOT, upload_file.image.name)

            # PyTorch 모델로 이미지 분석
            model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
            # model = torch.load('/Users/uiw_min/Downloads/yolov5s.pt')

            # model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
            results = model(img_path)
            df = results.pandas().xyxy[0].to_dict(orient='records')

            # 분석 결과 처리
            # 예: 결과를 데이터베이스에 저장하거나, 사용자에게 직접 보여주기
            request.session['analysis_result'] = df
            print(df)
            # # 업로드된 이미지의 URL을 세션에 저장
            # image_url = upload_file.image.url  # 업로드된 이미지의 URL
            # request.session['uploaded_image_url'] = request.build_absolute_uri(image_url)
            
            return redirect('app1:index')
    else:
        form = ImageUploadForm()
    return render(request, 'index.html', {'form': form})


@login_required
def add_score(request):
    user = request.user
    score, created = Score.objects.get_or_create(user=request.user)
    score.points += 5
    score.save()
    return redirect('app1:index')  # 점수 추가 후 리다이렉트할 페이지의 이름

@login_required(login_url='accounts:login')
def home(request):
     # 사용자의 점수 조회
    try:
        score = Score.objects.get(user=request.user)
    except Score.DoesNotExist:
        score = Score.objects.create(user=request.user, points=0)  # Score 객체가 없는 경우 생성

    # 점수를 컨텍스트에 추가하여 템플릿으로 전달
    context = {'score': score}
    return render(request, 'index.html', context)