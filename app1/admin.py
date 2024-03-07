from django.contrib import admin
from .models import UploadFile, TotalScore

# Register your models here.
admin.site.register(UploadFile)
admin.site.register(TotalScore)