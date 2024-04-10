from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True)
    nickname = models.CharField(max_length=31)

    def __str__(self):
        return self.user.get_username()


class Question(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField(max_length=1000)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField('Tag', related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Answer(models.Model):
    text = models.TextField(max_length=1000)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Answer of {self.author}'


class Tag(models.Model):
    name = models.SlugField(max_length=15, unique=True)

    def __str__(self):
        return self.name


class QuestionVote(models.Model):
    voter = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['question']),
        ]
        unique_together = ('author', 'question')

    def __str__(self):
        return f'Vote of {self.voter} for {self.question}'


class AnswerVote(models.Model):
    voter = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['answer']),
        ]
        unique_together = ('author', 'answer')

    def __str__(self):
        return f'Vote of {self.voter} for {self.answer}'
