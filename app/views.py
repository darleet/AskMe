from django.core.paginator import Paginator
from django.shortcuts import render


# Create your views here.
QUESTIONS = [
    {
        "id": i,
        "title": f"Question {i}",
        "text": f"This is question number {i}"
    } for i in range(200)
]

ANSWERS = [
    {
        "id": i,
        "text": f"This is answer number {i}"
    } for i in range(100)
]


def index(request):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(QUESTIONS, 5)
    page = paginator.page(page_num)
    return render(request, 'index.html', {'questions': page})


def question(request, question_id):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(ANSWERS, 5)
    page = paginator.page(page_num)
    return render(request, 'question.html', {
        'question': QUESTIONS[question_id], 'answers': page})
