from django.shortcuts import render
# from .models import Score # 이 줄은 제거
from app1.models import TotalScore

def ranking_view(request):
    scores = TotalScore.objects.all().order_by('-total_score')
    return render(request, 'ranking.html', {'scores': scores})
