import requests
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .models import Provider
from user_profile.models import Profile


def kakao_code_req(request):
    # 카카오 서버에 인증코드(code)를 요청한다.
    _restApiKey = '15cf5ee39e8fdc9a7284d70b6b8a7570'
    _redirectUrl = 'http://127.0.0.1:8000/account/kakao_token_req'
    _url = f'https://kauth.kakao.com/oauth/authorize?client_id={_restApiKey}&redirect_uri={_redirectUrl}&response_type=code'
    # 리턴값은 인가코드
    return redirect(_url)

def kakao_token_req(request):
    # 인증코드로 토큰를 요청한다
    _qs = request.GET['code']
    _restApiKey = '15cf5ee39e8fdc9a7284d70b6b8a7570'
    _redirect_uri = 'http://127.0.0.1:8000/account/kakao_token_req'
    _url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={_restApiKey}&redirect_uri={_redirect_uri}&code={_qs}'
    # post 방식으로 kakao서버에 받은 인종코드와 함께 토큰을 요청한다
    _res = requests.post(_url)
    _result = _res.json()
    print('_result: ', _result)
    request.session['access_token'] = _result['access_token']

    request.session.modified = True
    access_token = _result.get("access_token")
    # 받은 토큰으로 kapi 호출한다
    profile_request = requests.get("https://kapi.kakao.com/v2/user/me",
             headers={"Authorization": f"Bearer {access_token}"},)
    profile_json = profile_request.json()

    # 카카오 프로필을 가져오고 컨텍스트에 저장
    context = {}

    kakao_account = profile_json.get("kakao_account")
    email = kakao_account.get("email", None)
    profile = kakao_account.get("profile")
    username = email.split("@")[0]
    provider = 'kakao'

    return register_social_user(request, provider, username, email)


def register_social_user(request, provider, username, email):
    check_user_by_email = User.objects.filter(email=email)
    if check_user_by_email.exists():
        user = get_object_or_404(User, email=email)
        this_user_provider = get_object_or_404(Provider, user_id=user.id)
        if provider == this_user_provider.provider_name:
            registered_user = authenticate(username=username, password='temp_password')
            print('가입된 유저')
            login(request, registered_user)
            return redirect('index')
        else:
            messages.info(request, '이미 이 메일 주소를 사용하고 있는 사용자가 있습니다. '
                                   '새로운 계정으로 회원가입하세요')
            return redirect('/account/signup')


    else:
        print('신규유저')
        user = {
            'username': username,
            'email': email,
            'password': 'temp_password'
        }
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.save()
        this_user_provider = Provider.objects.create(user_id=user.id, provider_name=provider)
        this_user_profile = Profile.objects.create(user_id=user.id)
        this_user_provider.save()
        this_user_profile.save()
        new_user = authenticate(username=username, password='temp_password')
        login(request, new_user)
        print(new_user)

        return redirect('index')


def kakao_logout(request):
    _token = request.session['access_token']
    _url = 'https://kapi.kakao.com/v1/user/logout'
    _header = {
      'Authorization': f'Bearer {_token}'
    }
    _res = requests.post(_url, headers=_header)
    _result = _res.json()
    print(_result)
    if _result.get('id'):
        del request.session['access_token']
        return redirect('index')
    else:
        return render(request, 'account/logoutError.html')

