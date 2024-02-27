from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.http import HttpResponse


User = get_user_model()

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password == password_confirm:
            # 비밀번호 확인이 일치하면 사용자 계정 생성
            User.objects.create_user(username=username, email=email, password=password)
            # 회원가입 성공 후 로그인 페이지로 리디렉션
            return redirect('accounts:login')  # 로그인 URL로 변경하세요.
        else:
            # 비밀번호 불일치 처리
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
    else:
        # GET 요청 시 회원가입 폼을 렌더링
        return render(request, 'signup.html')



def login_view(request):  # 함수 이름 변경
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # 이름 충돌 없이 함수 호출
                return redirect('app1:index')  # 홈페이지 URL 이름 확인
            else:
                # 로그인 실패 시 사용자에게 에러 메시지 표시
                form.add_error(None, 'Username or password is incorrect')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    # 사용자를 로그아웃하고 홈페이지로 리다이렉트합니다.
    # 'home'은 홈페이지의 URL name입니다. 이를 원하는 대로 변경하세요.
    return redirect('app1:index')