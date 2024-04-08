from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'index.html')


def question(request, question_id):
    return render(request, 'question.html')
