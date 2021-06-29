from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from ..models import Question
from ..forms import QuestionForm



@login_required(login_url='account:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('posting:detail', question_id=question.id)
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'posting/question_form.html', context)


@login_required(login_url='account:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.author:
        messages.error(request, '이 글을 수정할 권한이 없습니다.')
        return redirect('posting:detail', question_id=question_id)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('posting:detail', question_id=question.id)

    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'posting/question_form.html', context)


@login_required(login_url='account:login')
def question_delete(request, question_id):
    """
    게시물 삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '이 글을 삭제할 권한이 없습니다.')
        return redirect('posting:detail', question_id=question.id)
    question.delete()
    return redirect('posting:index')
