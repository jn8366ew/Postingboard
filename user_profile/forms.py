from django import forms
from .models import Profile


class CreateUserProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(required=False, error_messages={'invalid': ("Image files only")},
                                   widget=forms.FileInput)
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic', 'website_url', 'facebook_url', 'twitter_url']
        labels = {
            'bio': '소개',
            'profile_pic': '프로필사진',
            'website_url': '개인웹사이트',
            'facebook_url': '페이스북',
            'twitter_url' : '트위터',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 5, 'cols': 50}),
            'website_url': forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'cols': 10}),
            'facebook_url': forms.Textarea(attrs={'class': 'form-control'}),
            'twitter_url': forms.Textarea(attrs={'class': 'form-control'}),
        }


# 에디트 폼 클래스 구현
class EditUserProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(required=False, error_messages= {'invalid': ("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic', 'website_url', 'facebook_url', 'twitter_url']
        labels = {
            'bio': '소개',
            'profile_pic': '프로필사진',
            'website_url': '개인웹사이트',
            'facebook_url': '페이스북',
            'twitter_url' : '트위터',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 5, 'cols': 50}),
            'website_url': forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'cols': 10}),
            'facebook_url': forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'cols': 10}),
            'twitter_url': forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'cols': 10}),
        }