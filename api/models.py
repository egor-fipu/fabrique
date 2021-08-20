from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

TYPES = (
    ('Text', 'Текстовый вопрос'),
    ('One_choice', 'С одним вариантом ответа'),
    ('Many_choice', 'С несколькими вариантами ответа'),
)


class Poll(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField(auto_now_add=True, editable=False)
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    text = models.TextField()
    type = models.CharField(max_length=11, choices=TYPES)
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    def __str__(self):
        return f'{self.text} ({self.type})'


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        related_name='choices',
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=200)

    def __str__(self):
        return f'id:{self.id}, {self.text}'


class Answer(models.Model):
    test = models.ForeignKey(
        'Test',
        on_delete=models.CASCADE,
        related_name='answers'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    choice = models.ManyToManyField(
        Choice,
        through='ChoiceAnswer',
        related_name='answers'
    )
    text = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.text}, {self.choice}'


class ChoiceAnswer(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)


class Test(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    id_user = models.PositiveIntegerField()
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name='tests'
    )
    created = models.DateTimeField(
        'Дата прохождения',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return f'{self.id_user}, {self.poll}'
