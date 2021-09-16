from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model


def create_user_api(client):
    data = {
        'username': 'TestUser',
        'password': 'test_password'
    }
    client.post('/auth/users/', data=data)
    user = get_user_model().objects.get(username=data['username'])
    return user


def auth_client(user):
    refresh = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


def create_polls(admin_client):
    result = []
    data = {
        "is_active": True,
        "title": "Первый опрос",
        "description": "Описание первого опроса"
    }
    response = admin_client.post('/api/polls/', data=data)
    data['id'] = response.json()['id']
    result.append(data)
    data = {
        "is_active": True,
        "title": "Второй опрос",
        "description": "Описание второго опроса"
    }
    response = admin_client.post('/api/polls/', data=data)
    data['id'] = response.json()['id']
    result.append(data)
    return result


def create_questions(admin_client):
    def create_question(uclient, poll_id, type, text):
        data = {
            'type': type,
            'text': text
        }
        response = uclient.post(f'/api/polls/{poll_id}/questions/', data=data)
        return response.json()['id']

    polls = create_polls(admin_client)
    result = list()

    result.append({
        'id': create_question(
            admin_client,
            polls[0]["id"],
            'Text',
            'Первый вопрос',
        ),
        'type': 'Text',
        'text': 'Первый вопрос',
        'choices': []
    })
    result.append({
        'id': create_question(
            admin_client,
            polls[0]["id"],
            'One_choice',
            'Второй вопрос'
        ),
        'type': 'One_choice',
        'text': 'Второй вопрос'
    })
    result.append({
        'id': create_question(
            admin_client,
            polls[0]["id"],
            'Many_choices',
            'Третий вопрос'
        ),
        'type': 'Many_choices',
        'text': 'Третий вопрос'
    })
    return result, polls


def create_choices(admin_client):
    def create_choice(uclient, poll_id, question_id, text):
        data = {
            'text': text
        }
        response = uclient.post(f'/api/polls/{poll_id}/questions/{question_id}/choices/', data=data)
        return response.json()['id']

    questions, polls = create_questions(admin_client)
    result = list()

    for index_q in range(1, len(questions)):
        result.append({
            'id': create_choice(admin_client, polls[0]["id"], questions[index_q]["id"], 'Первый вариант ответа'),
            'text': 'Первый вариант ответа'
        })
        result.append({
            'id': create_choice(admin_client, polls[0]["id"], questions[index_q]["id"], 'Второй вариант ответа'),
            'text': 'Второй вариант ответа'
        })
        result.append({
            'id': create_choice(admin_client, polls[0]["id"], questions[index_q]["id"], 'Третий вариант ответа'),
            'text': 'Третий вариант ответа'
        })
    # result.append({
    #     'id': create_choice(admin_client, polls[0]["id"], questions[2]["id"], 'Первый вариант ответа'),
    #     'text': 'Первый вариант ответа'
    # })
    # result.append({
    #     'id': create_choice(admin_client, polls[0]["id"], questions[2]["id"], 'Второй вариант ответа'),
    #     'text': 'Второй вариант ответа'
    # })
    # result.append({
    #     'id': create_choice(admin_client, polls[0]["id"], questions[2]["id"], 'Третий вариант ответа'),
    #     'text': 'Третий вариант ответа'
    # })
    return result, questions, polls
