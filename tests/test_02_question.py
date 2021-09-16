import pytest

from .common import (auth_client, create_polls, create_questions, create_choices, create_user_api)


class TestQuestionAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_questions_not_auth(self, client, admin_client):
        polls = create_polls(admin_client)
        response = admin_client.get(f'/api/polls/{polls[0]["id"]}/questions/')
        assert response.status_code != 404, (
            'Страница `/api/polls/{poll_id}/questions/` не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/questions/` суперюзера с токеном возвращается статус 200'
        )

        response = client.get(f'/api/polls/{polls[0]["id"]}/questions/')
        assert response.status_code == 401, (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/questions/` '
            'без токена авторизации возвращается статус 401'
        )

        user = create_user_api(client)
        client_user = auth_client(user)
        response = client_user.get(f'/api/polls/{polls[0]["id"]}/questions/')
        assert response.status_code == 403, (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/questions/` '
            'не суперюзера с токеном возвращается статус 403'
        )

    @pytest.mark.django_db(transaction=True)
    def test_02_questions_admin(self, admin_client):
        polls = create_polls(admin_client)
        data = {}
        response = admin_client.post(f'/api/polls/{polls[0]["id"]}/questions/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/polls/{poll_id}/questions/` с не правильными данными возвращает статус 400'
        )

        data = {
            'type': 'One_choice',
            'text': 'Первый вопрос'
        }
        response = admin_client.post(f'/api/polls/{polls[0]["id"]}/questions/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе `/api/polls/{poll_id}/questions/` с правильными данными возвращает статус 201'
        )

        data = {
            'type': 'Invalid_choice',
            'text': 'Первый вопрос'
        }
        response = admin_client.post(f'/api/polls/{polls[0]["id"]}/questions/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/polls/{poll_id}/questions/` поле type валидируется, '
            'с не правильными данными возвращает статус 400'
        )

        data = {
            'type': 'Many_choices',
            'text': 'Второй вопрос'
        }
        response = admin_client.post(f'/api/polls/{polls[0]["id"]}/questions/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе `/api/polls/{poll_id}/questions/` с правильными данными возвращает статус 201'
        )
        assert type(response.json().get('id')) == int, (
            'Проверьте, что при POST запросе `/api/polls/{poll_id}/questions/` возвращаете данные созданного объекта. '
            'Значение `id` нет или не является целым числом.'
        )

        response = admin_client.get(f'/api/polls/{polls[0]["id"]}/questions/')
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/questions/` возвращает статус 200'
        )

    @pytest.mark.django_db(transaction=True)
    def test_03_question_detail(self, admin_client):
        questions, polls = create_questions(admin_client)
        response = admin_client.get(f'/api/polls/{polls[0]["id"]}/questions/{questions[0]["id"]}/')
        assert response.status_code != 404, (
            'Страница `/api/polls/{poll_id}/questions/{question_id}/` не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/questions/{question_id}/` '
            'суперюзером возвращается статус 200'
        )
        data = response.json()
        assert type(data.get('id')) == int, (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/questions/{question_id}/` возвращаете данные объекта. '
            'Значение `id` нет или не является целым числом.'
        )
        assert data.get('text') == questions[0]['text'], (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/questions/{question_id}/` возвращаете данные объекта. '
            'Значение `text` неправильное.'
        )
        assert data.get('type') == questions[0]['type'], (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/questions/{question_id}/` возвращаете данные объекта. '
            'Значение `type` неправильное.'
        )

        data = {
            'type': 'One_choice',
            'text': 'Текст вопроса'
        }
        response = admin_client.patch(f'/api/polls/{polls[0]["id"]}/questions/{questions[0]["id"]}/', data=data)
        assert response.status_code == 200, (
            'Проверьте, что при PATCH запросе `/api/polls/{poll_id}/questions/{question_id}/` возвращается статус 200'
        )
        data = response.json()
        assert data.get('type') == 'One_choice', (
            'Проверьте, что при PATCH запросе `/api/polls/{poll_id}/questions/{question_id}/` возвращаете данные объекта. '
            'Значение `type` изменено.'
        )
        response = admin_client.get(f'/api/polls/{polls[0]["id"]}/questions/{questions[0]["id"]}/')
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/questions/{question_id}/` '
            'суперюзером возвращается статус 200'
        )
        data = response.json()
        assert data.get('type') == 'One_choice', (
            'Проверьте, что при PATCH запросе `/api/polls/{poll_id}/questions/{question_id}/` изменяет значение `type`.'
        )
        assert data.get('text') == 'Текст вопроса', (
            'Проверьте, что при PATCH запросе `/api/polls/{poll_id}/questions/{question_id}/` изменяет значение `text`.'
        )
        response = admin_client.delete(f'/api/polls/{polls[0]["id"]}/questions/{questions[0]["id"]}/')
        assert response.status_code == 204, (
            'Проверьте, что при DELETE запросе `/api/polls/{poll_id}/questions/{question_id}/` возвращает статус 204'
        )
        response = admin_client.get(f'/api/polls/{polls[0]["id"]}/questions/')
        test_data = response.json()
        assert len(test_data) == len(questions) - 1, (
            'Проверьте, что при DELETE запросе `/api/polls/{poll_id}/questions/` удаляет объект'
        )
