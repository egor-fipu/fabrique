from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import PollViewSet, QuestionViewSet, ChoiceViewSet, \
    UserPollViewSet, UserTestViewSet

router = SimpleRouter()

router.register('polls', PollViewSet, basename='poll')
router.register(
    r'polls/(?P<poll_id>\d+)/questions',
    QuestionViewSet,
    basename='question'
)
router.register(
    r'polls/(?P<poll_id>\d+)/questions/(?P<question_id>\d+)/choices',
    ChoiceViewSet,
    basename='choice'
)
# Для пользователей #
router.register('users/polls', UserPollViewSet, basename='users_poll')
router.register('users/tests', UserTestViewSet, basename='users_test')

urlpatterns = [
    path('', include(router.urls)),
]
