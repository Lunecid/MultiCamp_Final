
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'app1'

urlpatterns = [
    path('',views.main, name='main'),
    path('index/', views.index, name='index'),
    path('upload/', views.image_upload, name='image_upload'),
    path('addscore/', views.add_score, name='addscore'),
    path('home/', views.home, name='home'),  # 예시 URL 패턴

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)