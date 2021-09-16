from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from .mixins import CreateRetrieveViewSet
from .models import Poll, Question, Choice, Test
from .serializers import (PollSerializer, QuestionSerializer, ChoiceSerializer,
                          PollListSerializer, UserPollSerializer,
                          UserPollListSerializer, UserTestSerializer,
                          UserTestViewSerializer)


class PollViewSet(viewsets.ModelViewSet):
    """Добавление, редактирование, удаление опросов"""
    queryset = Poll.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return PollListSerializer
        return PollSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    """Добавление, редактирование, удаление вопросов в опросе"""
    serializer_class = QuestionSerializer

    def get_queryset(self):
        poll_id = self.kwargs.get('poll_id')
        get_object_or_404(Poll, id=poll_id)
        new_queryset = Question.objects.filter(poll=poll_id)
        return new_queryset

    def perform_create(self, serializer):
        poll_id = self.kwargs.get('poll_id')
        poll = get_object_or_404(Poll, id=poll_id)
        serializer.save(poll=poll)

    def perform_update(self, serializer):
        poll_id = self.kwargs.get('poll_id')
        poll = get_object_or_404(Poll, id=poll_id)
        serializer.save(poll=poll)


class ChoiceViewSet(viewsets.ModelViewSet):
    """Добавление, редактирование, удаление вариантов ответов в вопросе"""
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        poll_id = self.kwargs.get('poll_id')
        question_id = self.kwargs.get('question_id')
        get_object_or_404(Question, id=question_id, poll_id=poll_id)
        new_queryset = Choice.objects.filter(question=question_id)
        return new_queryset

    def perform_create(self, serializer):
        poll_id = self.kwargs.get('poll_id')
        question_id = self.kwargs.get('question_id')
        question = get_object_or_404(Question, id=question_id, poll_id=poll_id)
        serializer.save(question=question)

    def perform_update(self, serializer):
        poll_id = self.kwargs.get('poll_id')
        question_id = self.kwargs.get('question_id')
        question = get_object_or_404(Question, id=question_id, poll_id=poll_id)
        serializer.save(question=question)


# Для пользователей #


class UserPollViewSet(viewsets.ReadOnlyModelViewSet):
    """Просмотр активных опросов для пользователей"""
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        new_queryset = Poll.objects.filter(is_active=True)
        return new_queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return UserPollListSerializer
        return UserPollSerializer


class UserTestViewSet(CreateRetrieveViewSet):
    """Прохождение опроса, получение пройденных опросов"""
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'id_user'
    queryset = Test.objects.all()

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        new_queryset = queryset.filter(id_user=kwargs['id_user'])
        serializer = self.get_serializer(new_queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserTestViewSerializer
        return UserTestSerializer
