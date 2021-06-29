from django.urls import path, re_path
from .views import ShowProfilePageView, CreateProfilePageView, \
                    EditProfilePageView

app_name = 'user_profile'

urlpatterns = [
    re_path(r'^(?P<pk>\d+)/profile/$', ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile/', CreateProfilePageView.as_view(), name='create_profile'),
    re_path(r'^(?P<pk>\d+)/edit_profile/$', EditProfilePageView.as_view(), name='edit_profile'),

]