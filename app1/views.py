from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import UploadFile
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


