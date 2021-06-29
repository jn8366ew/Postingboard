from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count, F

from ..models import Question, Answer, Category, Ip
from user_profile.models import Profile


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def index(request):

    # 입력인자
    page = request.GET.get('page', '1')
    keyword = request.GET.get('keyword', '')
    sort_type = request.GET.get('sort_type', 'recent')


    # 정렬 (추천순 // 답글 갯수순 // 작성순서순
    if sort_type == 'recommend':
        question_list = Question.objects.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif sort_type == 'popular':
        question_list = Question.objects.annotate(
            num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:
        question_list = Question.objects.order_by('-create_date')


    # 조회
    if keyword:
        question_list = question_list.filter(
            Q(subject__icontains=keyword) |
            Q(content__icontains=keyword) |
            Q(author__username__icontains=keyword) |
            Q(answer__author__username__icontains=keyword)
        ).distinct()

    #페이징 처리
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'keyword': keyword, 'sort_type': sort_type}
    return render(request, 'posting/question_list.html', context)



def detail(request, question_id):

    question = get_object_or_404(Question, pk=question_id)

    # 답글 페이징 처리
    page = request.GET.get('page', 1)
    paginator = Paginator(question.answer_set.all(), 5)
    page_obj = paginator.get_page(page)

    # ip 가져오기
    ip = get_client_ip(request)

    # 페이징 뷰(조회수)를 위한 IP 검사 시작
    if Ip.objects.filter(ip=ip).exists():

        q1 = Question.objects.get(pk=question_id)
        q1.views.add(Ip.objects.get(ip=ip))

    else:
        Ip.objects.create(ip=ip)
        q1 = Question.objects.get(pk=question_id)
        q1.views.add(Ip.objects.get(ip=ip))


    context = {'question': question, 'answer_list': page_obj, 'page': page}


    # answer 정렬 -> 미구현

    # 작성자 가져오기
    print("1.Question-User:" )


    return render(request, 'posting/question_detail.html', context)


# 좀 더 적절한 구현이 필요. 코드가 반복되고 있다.
def catlistbyid(request, category_id):

    # 입력인자
    page = request.GET.get('page', '1')
    keyword = request.GET.get('keyword', '')
    sort_type = request.GET.get('sort_type', 'recent')

    # 정렬
    if sort_type == 'recommend':
        question_list = Question.objects.filter(category__id=category_id).annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif sort_type == 'popular':
        question_list = Question.objects.filter(category__id=category_id).annotate(
            num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:
        question_list = Question.objects.filter(category__id=category_id).order_by('-create_date')

    # 조회
    if keyword:
        question_list = question_list.filter(
            Q(subject__icontains=keyword) |
            Q(content__icontains=keyword) |
            Q(author__username__icontains=keyword) |
            Q(answer__author__username__icontains=keyword)
        ).distinct()

    # 페이징 처리
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    question_list = Question.objects.filter(category__id=category_id)
    context = {'category_id':category_id, 'question_list': page_obj, 'page': page, 'keyword': keyword, 'sort_type':sort_type}
    return render(request, 'posting/category.html', context)
