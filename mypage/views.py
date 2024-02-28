from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app1.models import UploadFile
from app1.models import Score



@login_required
def my_page(request):
    # 현재 사용자의 모든 점수를 가져와 총합을 계산
    try:
        user_score = Score.objects.get(user=request.user).points
    except Score.DoesNotExist:
        user_score = 0  # 사용자가 점수를 가지고 있지 않은 경우 0으로 설정

    uploaded_files = UploadFile.objects.filter(user=request.user)  # 현재 사용자의 업로드한 파일만을 조회
    
    return render(request, 'mypage.html', {'uploaded_files': uploaded_files, 'user_score': user_score})