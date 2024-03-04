from django.urls import path
from .views import ranking_view

app_name='ranking'

urlpatterns = [
    # 기존의 URL 패턴들
    path('', ranking_view, name='ranking'),
]
