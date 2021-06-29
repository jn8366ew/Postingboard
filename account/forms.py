from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class UserForm(UserCreationForm):
    email = forms.EmailField(label='이메일')

    class Meta:
        model = User
        fields = ("username", "email")

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        # 모델폼에서 연결해주는 모델의 경우 User() 이라고 설정해도 되나, global settiings 오버라이딩을 통해서 인증 User 모델을 다른 모델로 변경할 수도 있음.
        # model = User
        model = get_user_model()
        fields = ['username', 'email']
