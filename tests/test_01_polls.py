import pytest

from .common import (auth_client, create_polls, create_questions, create_choices, create_user_api)


class TestPollAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_polls_not_auth(self, client, admin_client):
        response = admin_client.get('/api/polls/')
        assert response.status_code != 404, (
            'Страница `/api/polls/` не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/polls/` суперюзера с токеном возвращается статус 200'
        )

        response = client.get('/api/polls/')
        assert response.status_code == 401, (
            'Проверьте, что при GET запросе `/api/polls/` '
            'без токена авторизации возвращается статус 401'
        )

        user = create_user_api(client)
        client_user = auth_client(user)
        response = client_user.get('/api/polls/')
        assert response.status_code == 403, (
            'Проверьте, что при GET запросе `/api/polls/` '
            'не суперюзера с токеном возвращается статус 403'
        )

    @pytest.mark.django_db(transaction=True)
    def test_02_polls_admin(self, admin_client):
        data = {}
        response = admin_client.post('/api/polls/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/polls/` с не правильными данными возвращает статус 400'
        )

        data = {
            'is_active': True,
            'title': 'Новый опрос',
            'description': 'Описание нового опроса'
        }
        response = admin_client.post('/api/polls/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе `/api/polls/` с правильными данными возвращает статус 201'
        )

        data = {
            'is_active': False,
            'title': 'Второй новый опрос',
            'description': 'Описание второго нового опроса'
        }
        response = admin_client.post('/api/polls/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе `/api/polls/` с правильными данными возвращает статус 201'
        )

        response = admin_client.get('/api/polls/')
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/polls/` возвращает статус 200'
        )

    @pytest.mark.django_db(transaction=True)
    def test_03_polls_delete_admin(self, admin_client):
        polls = create_polls(admin_client)
        response = admin_client.delete(f'/api/polls/{polls[1]["id"]}/')
        assert response.status_code == 204, (
            'Проверьте, что при DELETE запросе `/api/polls/{poll_id}/` возвращает статус 204'
        )
        response = admin_client.get('/api/polls/')
        test_data = response.json()
        assert len(test_data) == 1, (
            'Проверьте, что при DELETE запросе `/api/polls/{poll_id}/` удаляется опрос '
        )

        response = admin_client.get(f'/api/polls/{polls[1]["id"]}/')
        assert response.status_code == 404, (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/` возвращаете статус 404'
        )

        response = admin_client.patch(f'/api/polls/{polls[1]["id"]}/')
        assert response.status_code == 404, (
            'Проверьте, что при PATCH запросе `/api/polls/{poll_id}/` возвращаете статус 404'
        )
