from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app1.models import UploadFile
from app1.models import TotalScore



@login_required
def my_page(request):
    # 현재 사용자의 모든 점수를 가져와 총합을 계산
    try:
        total_score = TotalScore.objects.filter(user=request.user).first()
        normalized_score = (TotalScore / 1000) * 100
    except TotalScore.DoesNotExist:
        TotalScore = 0  # 사용자가 점수를 가지고 있지 않은 경우 0으로 설정

    # 현재 사용자가 업로드한 파일과 그에 따른 분석 점수 및 설명을 조회
    uploaded_files = UploadFile.objects.filter(user=request.user).all()
    context = {
        'uploaded_files': uploaded_files,
        'total_score': total_score.total_score if total_score else 0,
        'normalized_score': normalized_score,
    }
    
    return render(request, 'mypage.html', context)