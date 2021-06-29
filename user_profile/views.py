from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import AccessMixin
from django.views import generic
from django.urls import reverse_lazy
from .forms import CreateUserProfileForm, EditUserProfileForm

from .models import Profile
from posting.models import Question, Answer, Comment

# 프로필 보이기(클래스 베이스)

class OwnerOnlyMixin(AccessMixin):
    raise_exception = True
    permission_denied_message = "사용 권한이 없습니다"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ShowProfilePageView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'user_profile/show_profile.html'

    def get_context_data(self, *args, **kwargs):
        # users = Profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context["page_user"] = page_user

        # 특정유저의 질문 갯수 저장
        context["num_questions"] = Question.objects.filter(author__id = page_user.id).count()
        # 특정유저의 답글 갯수 저장
        context["num_answers"] = Answer.objects.filter(author__id=page_user.id).count()
        # 특정유저의 댓글 갯수 저장
        context["num_comments"] = Comment.objects.filter(author__id=page_user.id).count()

        return context

# 프로필 생성
class CreateProfilePageView(OwnerOnlyMixin, generic.CreateView):
    model = Profile
    form_class = CreateUserProfileForm
    template_name = 'user_profile/create_profile.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# 프로필 업데이트
class EditProfilePageView(OwnerOnlyMixin, generic.UpdateView):
    model = Profile
    form_class = EditUserProfileForm
    template_name = 'user_profile/edit_profile.html'
    # fields = ['bio', 'profile_pic', 'website_url', 'facebook_url', 'twitter_url']
    success_url = reverse_lazy('index')
