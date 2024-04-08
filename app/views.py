from django.shortcuts import render


# Create your views here.
QUESTIONS = [
    {
        "id": i,
        "title": f"Question {i}",
        "text": f"This is question number {i}"
    } for i in range(200)
]


def index(request):
    return render(request, 'index.html', {'questions': QUESTIONS})


def question(request, question_id):
    return render(request, 'question.html', {'question': QUESTIONS[question_id]})
