
from django.urls import path
from . import views


app_name = 'app1'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.image_upload, name='image_upload'),
    
]