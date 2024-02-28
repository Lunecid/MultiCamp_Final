from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "mypage"

urlpatterns = [
    path('my_page/', views.my_page, name='my_page'),
]
