from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app1.models import UploadFile
from app1.models import TotalScore


@login_required
def my_page(request):
    # 현재 사용자가 업로드한 파일과 그에 따른 분석 점수 및 설명을 조회
    uploaded_files = UploadFile.objects.filter(user=request.user).all()
    total_score = TotalScore.objects.filter(user=request.user).first()
    context = {
        'uploaded_files': uploaded_files,
        'total_score': total_score.total_score if total_score else 0,
    }

    return render(request, 'mypage.html', context)
