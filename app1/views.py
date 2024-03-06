from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import UploadFile,TotalScore
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
import os
import torch
from PIL import Image
import subprocess

from ultralytics import YOLO
import numpy as np



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
            upload_file_instance = form.save(commit=False)
            upload_file_instance.user = request.user
            upload_file_instance.save()  # UploadFile 모델의 save 메서드에서 추가 로직 처리

            uploaded_image_url = os.path.join(settings.MEDIA_URL, str(upload_file_instance.image))
            request.session['uploaded_image_url'] = uploaded_image_url
            
            # 이미지 분석 수행
            image_path = os.path.join(settings.MEDIA_ROOT, str(upload_file_instance.image))
            score, phrase = analyze_image(image_path)

            # 분석 결과를 UploadFile 인스턴스에 저장
            upload_file_instance.analysis_score = score
            upload_file_instance.analysis_phrase = phrase
            
            # 변경 사항 저장
            upload_file_instance.save()
            
            request.session['analysis_score'] = score
            request.session['analysis_phrase'] = phrase
    
            return redirect('app1:home')
    else:
        form = ImageUploadForm()
    return render(request, 'index.html', {'form': form})



def analyze_image(image_path):
    score = 0
    phrase = '분석 결과 없음'


    # -- 첫번째 모델 in, out 구분 
    model_Stand1 = YOLO('best.pt')
    results_Stand1 = model_Stand1(image_path)

    # Process results list
    for result in results_Stand1:
        uniq, cnt = np.unique(result.boxes.cls.cpu().numpy(), return_counts=True)

    # -- 두번째 모델 stand, fall 구분
    model_Stand2 = YOLO('kick_ScooterWheel.pt')
    results_Stand2 = model_Stand2(image_path)

    for _ in results_Stand2[0].boxes.data:
        if _[-1] == 1.0000e+00:
            height = results_Stand2[0].boxes.data[0][2] - results_Stand2[0].boxes.data[0][0]
            width = results_Stand2[0].boxes.data[0][3] - results_Stand2[0].boxes.data[0][1]

    if 2 in uniq:
        if width < height:
            score = 15        # 라인안에있고 stand
            phrase = '매우 적합'
        elif width > height:
            score = 11          # 라인안에있고 fail
            phrase = '적합'
    elif 1 in uniq:  
        if width < height:   # 라인밖 stand
            score = 9
            phrase = '보통'
        elif width > height:  #라인밖 fail
            score = 5
            phrase = '미흡'    

    return score, phrase


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
        total_score = TotalScore.objects.get(user=request.user)
    except TotalScore.DoesNotExist:
        total_score = TotalScore.objects.create(user=request.user, total_score=0)


    # 점수를 컨텍스트에 추가하여 템플릿으로 전달
    # context = {'score': score}
    context = {
        'total_score': total_score.total_score,
        'analysis_score': request.session.pop('analysis_score', None),
        'analysis_phrase': request.session.pop('analysis_phrase', None),
    }
    return render(request, 'index.html', context)