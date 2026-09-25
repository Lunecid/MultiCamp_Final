from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings


# Create your views here.
@login_required(login_url='accounts:login')
def index(request):
    return render(request, 'default.html', {'KAKAO_JS_KEY': settings.KAKAO_JS_KEY})