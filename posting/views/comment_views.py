from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from ..models import Question, Answer, Comment
from ..forms import CommentForm



@login_required(login_url='account:login')
def comment_create_question(request, question_id):
    """
    질문 댓글 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
            #return redirect('posting:detail', question_id=question.id)
            return redirect('{}#comment_{}'.format(resolve_url('posting:detail',
                                                               question_id=comment.question.id), comment.id))

    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'posting/comment_form.html', context)


@login_required(login_url='account:login')
def comment_modify_question(request, comment_id):
    """
    질문 댓글 변경
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '답글을 수정 할 권한이 없습니다')
        return redirect('posting:detail', question_id=comment.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            #return redirect('posting:detail', question_id=comment.question.id)
            return redirect('{}#comment_{}'.format(resolve_url('posting:detail',
                                                               question_id=comment.question.id), comment.id))

    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'posting/comment_form.html', context)


@login_required(login_url='account:login')
def comment_delete_question(request, comment_id):
    """
    댓글 삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글을 삭제 할 권한이 없습니다')
        return redirect('posting:detail', question_id=comment.question.id)
    else:
        comment.delete()
    return redirect('posting:detail', question_id=comment.question.id)


@login_required(login_url='account:login')
def comment_create_answer(request, answer_id):
    """
    답변 댓글 등록
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            return redirect('{}#comment_{}'.format(resolve_url('posting:detail',
                                                               question_id=comment.answer.question.id), comment.id))

    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'posting/comment_form.html', context)


@login_required(login_url='account:login')
def comment_modify_answer(request, comment_id):
    """
    질문 댓글 변경
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '답글을 수정 할 권한이 없습니다')
        return redirect('posting:detail', question_id=comment.answer.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(resolve_url('posting:detail',
                                                               question_id=comment.answer.question.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'posting/comment_form.html', context)


@login_required(login_url='account:login')
def comment_delete_answer(request, comment_id):
    """
    댓글 삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글을 삭제 할 권한이 없습니다')
        return redirect('posting:detail', question_id=comment.answer.question.id)
    else:
        comment.delete()
    return redirect('posting:detail', question_id=comment.answer.question.id)