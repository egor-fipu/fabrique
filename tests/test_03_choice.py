import pytest

from .common import (auth_client, create_polls, create_questions, create_choices, create_user_api)


class TestChoiceAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_choices_not_auth(self, client, admin_client):
        questions, polls = create_questions(admin_client)
        response = admin_client.get(
            f'/api/polls/{polls[0]["id"]}/questions/{questions[1]["id"]}/choices/'
        )
        assert response.status_code != 404, (
            'Страница `/api/polls/{poll_id}/questions/{question_id}/choices/` '
            'не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/questions/{question_id}/choices/` '
            'суперюзера с токеном возвращается статус 200'
        )

        response = client.get(
            f'/api/polls/{polls[0]["id"]}/questions/{questions[1]["id"]}/choices/'
        )
        assert response.status_code == 401, (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/questions/{question_id}/choices/` '
            'без токена авторизации возвращается статус 401'
        )

        user = create_user_api(client)
        client_user = auth_client(user)
        response = client_user.get(
            f'/api/polls/{polls[0]["id"]}/questions/{questions[1]["id"]}/choices/'
        )
        assert response.status_code == 403, (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/questions/{question_id}/choices/` '
            'не суперюзера с токеном возвращается статус 403'
        )

    @pytest.mark.django_db(transaction=True)
    def test_02_choices_admin(self, admin_client):
        questions, polls = create_questions(admin_client)
        data = {}
        response = admin_client.post(
            f'/api/polls/{polls[0]["id"]}/questions/{questions[1]["id"]}/choices/', data=data
        )
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/polls/{poll_id}/questions/'
            '{question_id}/choices/` с неправильными данными возвращает статус 400'
        )

        data = {
            'text': 'Вариант ответа'
        }
        response = admin_client.post(
            f'/api/polls/{polls[0]["id"]}/questions/{questions[1]["id"]}/choices/', data=data
        )
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе `/api/polls/{poll_id}/questions/{question_id}/choices/` '
            'с правильными данными возвращает статус 201'
        )

        data = {
            'text': ''
        }
        response = admin_client.post(
            f'/api/polls/{polls[0]["id"]}/questions/{questions[1]["id"]}/choices/', data=data
        )
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/polls/{poll_id}/questions/{question_id}/choices/` '
            'с не правильными данными возвращает статус 400'
        )

        data = {
            'text': 'Другой вариант ответа'
        }
        response = admin_client.post(
            f'/api/polls/{polls[0]["id"]}/questions/{questions[1]["id"]}/choices/', data=data
        )
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе `/api/polls/{poll_id}/questions/{question_id}/choices/` '
            'с правильными данными возвращает статус 201'
        )
        assert type(response.json().get('id')) == int, (
            'Проверьте, что при POST запросе `/api/polls/{poll_id}/questions/{question_id}/choices/` '
            'возвращаете данные созданного объекта. '
            'Значение `id` нет или не является целым числом.'
        )

        response = admin_client.post(
            f'/api/polls/{polls[0]["id"]}/questions/{questions[0]["id"]}/choices/', data=data
        )
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/polls/{poll_id}/questions/{question_id}/choices/` '
            'к вопросу типом Text нельзя добавить авриант ответа, возвращает статус 400'
        )

        response = admin_client.get(
            f'/api/polls/{polls[0]["id"]}/questions/{questions[1]["id"]}/choices/'
        )
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/questions/{question_id}/choices/` '
            'возвращает статус 200'
        )

    @pytest.mark.django_db(transaction=True)
    def test_03_choices_detail(self, admin_client):
        choices, questions, polls = create_choices(admin_client)
        response = admin_client.get(
            f'/api/polls/{polls[0]["id"]}/questions/{questions[1]["id"]}/choices/{choices[0]["id"]}/'
        )
        assert response.status_code != 404, (
            'Страница `/api/polls/{poll_id}/questions/{question_id}/choices/{choice_id}/` '
            'не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/questions/{question_id}/choices/{choice_id}/` '
            'суперюзером возвращается статус 200'
        )
        data = response.json()
        assert type(data.get('id')) == int, (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/questions/{question_id}/choices/{choice_id}/` '
            'возвращаете данные объекта. Значение `id` нет или не является целым числом.'
        )
        assert data.get('text') == choices[0]['text'], (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/questions/{question_id}/choices/{choice_id}/` '
            'возвращаете данные объекта. Значение `text` неправильное.'
        )

        data = {
            'text': 'Текст варианта'
        }
        response = admin_client.patch(
            f'/api/polls/{polls[0]["id"]}/questions/{questions[1]["id"]}/choices/{choices[0]["id"]}/', data=data
        )
        assert response.status_code == 200, (
            'Проверьте, что при PATCH запросе `/api/polls/{poll_id}/questions/{question_id}/choices/{choice_id}/` '
            'возвращается статус 200'
        )
        data = response.json()
        assert data.get('text') == 'Текст варианта', (
            'Проверьте, что при PATCH запросе `/api/polls/{poll_id}/questions/{question_id}/choices/{choice_id}/` '
            'возвращаете данные объекта. Значение `text` изменено.'
        )
        response = admin_client.get(
            f'/api/polls/{polls[0]["id"]}/questions/{questions[1]["id"]}/choices/{choices[0]["id"]}/'
        )
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/questions/{question_id}/choices/{choice_id}/` '
            'суперюзером возвращается статус 200'
        )
        data = response.json()
        assert data.get('text') == 'Текст варианта', (
            'Проверьте, что при PATCH запросе `/api/polls/{poll_id}/questions/{question_id}/choices/{choice_id}/` '
            'изменяет значение `text`.'
        )

        response = admin_client.delete(
            f'/api/polls/{polls[0]["id"]}/questions/{questions[1]["id"]}/choices/{choices[0]["id"]}/'
        )
        assert response.status_code == 204, (
            'Проверьте, что при DELETE запросе `/api/polls/{poll_id}/questions/{question_id}/choices/{choice_id}/` '
            'возвращает статус 204'
        )

        response = admin_client.get(
            f'/api/polls/{polls[0]["id"]}/questions/{questions[1]["id"]}/choices/'
        )
        test_data = response.json()
        assert len(test_data) == 2, (
            'Проверьте, что при DELETE запросе `/api/polls/{poll_id}/questions/{question_id}/choices/` удаляет объект'
        )
