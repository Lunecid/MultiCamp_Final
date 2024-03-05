from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission

# Create your models here.

class User(AbstractUser):
    # 사용자 모델에 대한 정의
    
    class Meta:
        # 다른 Meta 옵션과 함께 존재하는 경우 추가
        pass
    
        
# accounts.User 모델에 대한 그룹 및 사용자 권한 관련 역참조 이름 변경
User.groups.field.remote_field.related_name = 'custom_user_groups'
User.user_permissions.field.remote_field.related_name = 'custom_user_permissions'

# auth.User 모델에 대한 그룹 및 사용자 권한 관련 역참조 이름 변경
Group.user_set.field.remote_field.related_name = 'auth_group_user_set'
Permission.user_set.field.remote_field.related_name = 'auth_permission_user_set'
