from math import sqrt

from django.core.management.base import BaseCommand
from app.models import *


class Command(BaseCommand):
    help = 'Fills the database with initial data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='The ratio of data to fill (should be > 1)')

    def handle(self, *args, **options):
        ratio = options['ratio']
        if ratio <= 1:
            raise ValueError('Ratio should be > 1')

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
                question=questions[i % ratio],
                author=profiles[i % ratio],
            ) for i in range(ratio * 100)
        ]
        Answer.objects.bulk_create(answers)

        self.stdout.write(f'Creating votes...')
        rsqrt = int(sqrt(ratio))

        # ratio * 20 iterations
        qvotes = [
            QuestionVote(
                question=questions[i],
                voter=profiles[j],
                value=SCORES[0][0],
            ) for i in range(rsqrt * 20) for j in range(ratio - 1, ratio - 1 - rsqrt + i // 20, -1)
        ] + [
            QuestionVote(
                question=questions[i],
                voter=profiles[j],
                value=SCORES[1][0],
            ) for i in range(rsqrt * 20) for j in range(0, i // 20)
        ]
        QuestionVote.objects.bulk_create(qvotes)

        print(len(qvotes))

        # ratio * 180 iterations
        avotes = [
            AnswerVote(
                answer=answers[i],
                voter=profiles[j],
                value=SCORES[0][0],
            ) for i in range(rsqrt * 180) for j in range(ratio - 1, ratio - 1 - rsqrt + i // 180, -1)
        ] + [
            AnswerVote(
                answer=answers[i],
                voter=profiles[j],
                value=SCORES[1][0],
            ) for i in range(rsqrt * 180) for j in range(0, i // 180)
        ]
        AnswerVote.objects.bulk_create(avotes)

        print(len(avotes))

        self.stdout.write(
            self.style.SUCCESS(f'Database filled successfully'))
