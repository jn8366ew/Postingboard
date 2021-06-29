from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from .views import login_view, signup, find_email, \
                    result, change_password, \
                    password_change_done
from .kakao_login_view import kakao_logout, kakao_code_req, \
                            kakao_token_req


app_name = 'account'

urlpatterns = [
    path('login/', login_view.as_view(), name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('find_email/', find_email, name='find_email'),
    path('result/', result, name='result'),
    path('change_password/', change_password, name='change_password'),
    path('password_change_done/', password_change_done, name='password_change_done'),

    # 비밀번호 찾기 (수정 필요)
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="account/reset_password.html"),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="account/reset_password_sent.html"),
         name="reset_password_sent"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="account/reset_password_form.html"),
         name="reset_password_form"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="account/reset_password_complete.html"),
         name="reset_password_complete"),

    # 카카오로그인
    path('kakao_code_req/', kakao_code_req, name='kakao_code_req'),
    path('kakao_token_req/', kakao_token_req, name='kakao_token_req'),
    path('kakao_logout/', kakao_logout, name='kakao_logout'),


]