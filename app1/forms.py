# forms.py
from django import forms
from .models import UploadFile

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = ['image']
