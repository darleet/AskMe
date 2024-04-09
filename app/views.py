import datetime

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render


# Create your views here.
QUESTIONS = [
    {
        "id": i,
        "title": f"Question {i}",
        "text": f"This is question number {i}",
        "creation_date": datetime.datetime.now() - datetime.timedelta(days=i),
        "tags": [f"tag_{i % 5}"],
    } for i in range(200)
]

ANSWERS = [
    {
        "id": i,
        "text": f"This is answer number {i}"
    } for i in range(100)
]


def paginate(objects, request, per_page=10):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(objects, per_page)
    try:
        page = paginator.page(page_num)
    except (PageNotAnInteger, EmptyPage):
        page = paginator.page(1)
    return page


def index(request):
    page = paginate(QUESTIONS, request)
    return render(request, 'index.html', {'questions': page, 'filter': 0})


def hot(request):
    page = paginate(QUESTIONS, request)
    return render(request, 'index.html', {'questions': page, 'filter': 1})


def question(request, question_id):
    page = paginate(ANSWERS, request)
    return render(request, 'question.html',
                  {'question': QUESTIONS[question_id], 'answers': page})


def new_question(request):
    return render(request, 'new_question.html')


def settings(request):
    return render(request, 'settings.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def search_tag(request, tag):
    # select only questions with requested tag
    questions = [q for q in QUESTIONS if tag in q['tags']]
    page = paginate(questions, request)
    return render(request, 'index.html', {'questions': page, 'filter': 2, 'tag': tag})
