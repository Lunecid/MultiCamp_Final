from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import UploadFile,Score
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='accounts:login')
def index(request):
    return render(request, 'index.html')

@login_required(login_url='accounts:login')
def image_upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save() 대신 모델 인스턴스를 생성하고 저장하는 로직
            image = form.cleaned_data['image']
            new_file = UploadFile(image=image)  # UploadFile 모델 인스턴스 생성
            new_file.save()  # 모델 인스턴스 저장
            return redirect('app1:index')  # 성공 시 리디렉션할 뷰의 이름

    else:
        form = ImageUploadForm()
    return render(request, 'index.html', {'form': form})


@login_required
def add_score(request):
    score, created = Score.objects.get_or_create(user=request.user)
    score.points += 5
    score.save()
    return redirect('app1:index')  # 점수 추가 후 리다이렉트할 페이지의 이름

@login_required(login_url='accounts:login')
def home(request):
    # 사용자의 점수 조회
    try:
        score = Score.objects.get(user=request.user).points
    except Score.DoesNotExist:
        score = 0  # Score 객체가 없는 경우 점수를 0으로 설정

    # 점수를 컨텍스트에 추가하여 템플릿으로 전달
    return render(request, 'index.html', { 'points': score})
