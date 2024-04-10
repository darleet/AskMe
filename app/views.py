import datetime

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from app.models import Question


def paginate(objects, request, per_page=10):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(objects, per_page)
    try:
        page = paginator.page(page_num)
    except (PageNotAnInteger, EmptyPage):
        page = paginator.page(1)
    return page


def index(request):
    questions = Question.objects.get_latest()
    page = paginate(questions, request)
    return render(request, 'index.html', {'questions': page})


def hot(request):
    questions = Question.objects.get_hot()
    page = paginate(questions, request)
    return render(request, 'hot.html', {'questions': page})


def question(request, question_id):
    question_object = Question.objects.get_by_id(question_id)
    page = paginate(question_object['answers'], request)
    return render(request, 'question.html',
                  {'question': question, 'answers': page})


def new_question(request):
    return render(request, 'new_question.html')


def settings(request):
    return render(request, 'settings.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def search_tag(request, tag):
    questions = Question.objects.get_by_tag(tag)
    page = paginate(questions, request)
    return render(request, 'tag.html', {'questions': page, 'tag': tag})
