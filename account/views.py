import random
import string

from django.shortcuts import render
from .forms import UserForm
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import AccessMixin

from account.models import Provider
from user_profile.models import Profile


class login_view(auth_views.LoginView):
    template_name = 'account/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            self.redirect_field_name: self.get_redirect_url(),
            'site': current_site,
            'site_name': current_site.name,
            **(self.extra_context or {})
        })
        context['kakao_token_check'] = False
        if self.request.session.get('access_token'):
            context['kakao_token_check'] = True
        return context


def signup(request):
    #   회원가입
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)
            login(request, user)

            # 새로 만드는 Provider와 Profile 인스턴트 생성
            this_user = User.objects.get(username=username)
            this_user_profile = Profile.objects.create(user_id=this_user.id)
            this_user_provider = Provider.objects.create(user_id=this_user.id)
            this_user_profile.save()
            this_user_provider.save()
            return redirect('index')

    else:
        # Get 요청
        form = UserForm()

    return render(request, 'account/signup.html', {'form': form})



def find_email(request):
    context = {}
    return render(request, "account/find_email.html", context)


def result(request):
    context = {'email': request.GET.get('email')}
    emails = User.objects.filter(is_active=True).values_list('email', flat=True)

    source = string.ascii_letters + string.digits
    temp_pw = ''.join((random.choice(source) for i in range(8)))

    print(temp_pw)

    email_contents =  ['변경된' '패스워드는', temp_pw, '입니다']


    if context['email'] in emails:
        print(True)
        user_obj = User.objects.get(email=context['email'])
        user_obj.set_password(temp_pw)
        user_obj.save()
        user_obj.email_user(
            '[Important] 장고 실험 ',
                " ".join(email_contents),
                'MySite@example.com'
        )

    return render(request, "account/result.html", context)


@login_required(login_url='account:login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            logout(request)
            return redirect('/account/password_change_done')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change_password.html', {'form': form})


def password_change_done(request):
     context = {}
     return render(request, "account/password_change_done.html", context)