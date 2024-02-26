
from django.urls import path
from . import views


app_name = 'app1'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.image_upload, name='image_upload'),
    path('addscore/', views.add_score, name='addscore'),
    path('home/', views.home, name='home'),  # 예시 URL 패턴

    
]