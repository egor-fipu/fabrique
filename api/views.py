from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, mixins, permissions
from rest_framework.exceptions import APIException

from .models import Poll, Question, Choice, Test
from .serializers import PollSerializer, QuestionSerializer, ChoiceSerializer, \
    PollListSerializer, UserPollSerializer, UserPollListSerializer, \
    UserTestSerializer, UserTestViewSerializer


class PollViewSet(viewsets.ModelViewSet):
    """Добавление, редактирование, удаление опросов"""
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return PollListSerializer
        return PollSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    """Добавление, редактирование, удаление вопросов в опросе"""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        poll_id = self.kwargs.get('poll_id')
        try:
            Poll.objects.get(id=poll_id)
        except ObjectDoesNotExist:
            raise APIException('Страница не найдена.')
        new_queryset = Question.objects.filter(poll=poll_id)
        return new_queryset

    def perform_create(self, serializer):
        poll_id = self.kwargs.get('poll_id')
        try:
            poll = Poll.objects.get(id=poll_id)
        except ObjectDoesNotExist:
            raise APIException('Страница не найдена.')
        serializer.save(poll=poll)

    def perform_update(self, serializer):
        poll_id = self.kwargs.get('poll_id')
        try:
            poll = Poll.objects.get(id=poll_id)
        except ObjectDoesNotExist:
            raise APIException('Страница не найдена.')
        serializer.save(poll=poll)


class ChoiceViewSet(viewsets.ModelViewSet):
    """Добавление, редактирование, удаление вариантов ответов в вопросе"""
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        poll_id = self.kwargs.get('poll_id')
        question_id = self.kwargs.get('question_id')
        try:
            Poll.objects.get(id=poll_id)
            Question.objects.get(id=question_id)
        except ObjectDoesNotExist:
            raise APIException('Страница не найдена.')
        new_queryset = Choice.objects.filter(question=question_id)
        return new_queryset

    def perform_create(self, serializer):
        poll_id = self.kwargs.get('poll_id')
        question_id = self.kwargs.get('question_id')
        try:
            Poll.objects.get(id=poll_id)
            question = Question.objects.get(id=question_id)
        except ObjectDoesNotExist:
            raise APIException('Страница не найдена.')
        serializer.save(question=question)

    def perform_update(self, serializer):
        poll_id = self.kwargs.get('poll_id')
        question_id = self.kwargs.get('question_id')
        try:
            Poll.objects.get(id=poll_id)
            question = Question.objects.get(id=question_id)
        except ObjectDoesNotExist:
            raise APIException('Страница не найдена.')
        serializer.save(question=question)


# Для пользователей #


class UserPollViewSet(viewsets.ReadOnlyModelViewSet):
    """Просмотр активных опросов для пользователей"""
    queryset = Poll.objects.all()
    serializer_class = UserPollSerializer
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        if self.action == 'list':
            return UserPollListSerializer
        return UserPollSerializer

    def get_queryset(self):
        new_queryset = Poll.objects.filter(is_active=True)
        return new_queryset


class CreateListViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    pass


class UserTestViewSet(CreateListViewSet):
    """Прохождение опроса, получение пройденных опросов"""
    serializer_class = UserTestSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        id_user = self.request.query_params.get('user')
        if id_user is not None:
            queryset = Test.objects.filter(id_user=id_user)
            if queryset:
                return queryset
            else:
                raise APIException(
                    f'Пользователя с <id_user> "{id_user}" не существует'
                )
        else:
            raise APIException(
                'Для получения пройденных тестов в запросе необходимо указать '
                'id_user: http://127.0.0.1:8000/api/users/tests/?user=<id_user>'
            )

    def get_serializer_class(self):
        if self.action == 'list':
            return UserTestViewSerializer
        return UserTestSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()

