from django.shortcuts import render
# from .models import Score # 이 줄은 제거
from app1.models import Score

def ranking_view(request):
    scores = Score.objects.order_by('-points')  # 점수가 높은 순으로 정렬
    return render(request, 'ranking.html', {'scores': scores})
