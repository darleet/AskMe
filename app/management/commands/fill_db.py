from django.core.management.base import BaseCommand
from app.models import *

from random import shuffle


class Command(BaseCommand):
    help = 'Fills the database with initial data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='The ratio of data to fill')

    def handle(self, *args, **options):
        ratio = options['ratio']

        Tag.objects.all().delete()
        User.objects.all().delete()
        Profile.objects.all().delete()
        Question.objects.all().delete()
        Answer.objects.all().delete()
        QuestionVote.objects.all().delete()
        AnswerVote.objects.all().delete()

        self.stdout.write(f'Creating tags...')
        tags = [Tag(name=f'tag_{i}') for i in range(ratio)]
        Tag.objects.bulk_create(tags)

        self.stdout.write(f'Creating profiles...')
        users = [
            User(
                username=f'user_{i}',
                password='django-test1234',
                email=f'user_{i}@example.com',
            ) for i in range(ratio)
        ]
        User.objects.bulk_create(users)
        profiles = [
            Profile(
                user=users[i],
                nickname=f'user_{i}',
            ) for i in range(ratio)
        ]
        Profile.objects.bulk_create(profiles)

        self.stdout.write(f'Creating questions...')
        questions = [
            Question(
                title=f'Question {i}',
                text=f'This is question number {i}',
                author=profiles[i % ratio],
            ) for i in range(ratio * 10)
        ]
        Question.objects.bulk_create(questions)
        for i in range(len(questions)):
            questions[i].tags.add(tags[i % ratio])

        self.stdout.write(f'Creating answers...')
        answers = [
            Answer(
                text=f'This is answer number {i}',
                question=questions[i % (ratio * 10)],
                author=profiles[i % ratio],
            ) for i in range(ratio * 100)
        ]
        Answer.objects.bulk_create(answers)

        self.stdout.write(f'Creating votes...')
        qvotes = [
            QuestionVote(
                question=questions[j],
                voter=profiles[i],
                value=SCORES[i // (ratio * 80)][0],
            ) for i in range(ratio) for j in range(10)
        ]
        QuestionVote.objects.bulk_create(qvotes)
        avotes = [
            AnswerVote(
                answer=answers[j],
                voter=profiles[i],
                value=SCORES[i // (ratio * 80)][0],
            ) for i in range(ratio) for j in range(100)
        ]
        AnswerVote.objects.bulk_create(avotes)

        self.stdout.write(
            self.style.SUCCESS(f'Database filled successfully'))
