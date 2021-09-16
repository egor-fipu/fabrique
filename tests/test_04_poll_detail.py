import datetime

import pytest


from .common import (auth_client, create_polls, create_questions, create_choices, create_user_api)


class TestPollDetailAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_poll_detail(self, admin_client):
        choices, questions, polls = create_choices(admin_client)
        response = admin_client.get(
            f'/api/polls/{polls[0]["id"]}/')
        assert response.status_code != 404, (
            'Страница `/api/polls/{poll_id}/` не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/` '
            'суперюзером возвращается статус 200'
        )
        data = response.json()
        assert type(data.get('id')) == int, (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/` возвращаете данные объекта. '
            'Значение `id` нет или не является целым числом.'
        )
        assert data.get('is_active') == polls[0]['is_active'], (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/` возвращаете данные объекта. '
            'Значение `is_active` неправильное.'
        )
        assert 'start_date' in data and data.get('start_date') is not None, (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/` возвращаете данные объекта. '
            'Значение `start_date` отсутствует или null'
        )
        assert 'end_date' in data, (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/` возвращаете данные объекта. '
            'Значение `end_date` отсутствует'
        )
        assert data.get('title') == polls[0]['title'], (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/` возвращаете данные объекта. '
            'Значение `title` неправильное.'
        )
        assert data.get('description') == polls[0]['description'], (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/` возвращаете данные объекта. '
            'Значение `description` неправильное.'
        )
        assert 'questions' in data, (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/` возвращаете данные объекта. '
            'Значение `questions` отсутствует'
        )
        assert data.get('questions')[0] == questions[0], (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/` возвращаете данные объекта. '
            'Значение `questions` `questions` неправильное.'
        )
        assert data.get('questions')[1].get('id') == questions[1]['id'], (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/` возвращаете данные объекта. '
            'Значение `id` `questions` неправильное.'
        )
        assert data.get('questions')[1].get('type') == questions[1]['type'], (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/` возвращаете данные объекта. '
            'Значение `type` `questions` неправильное.'
        )
        assert data.get('questions')[1].get('text') == questions[1]['text'], (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/` возвращаете данные объекта. '
            'Значение `text` `questions` неправильное.'
        )
        assert 'choices' in data.get('questions')[1], (
            'Проверьте, что при GET запросе `/api/polls/{poll_id}/` возвращаете данные объекта. '
            'Значение `choices` в `questions` отсутствует'
        )
        test_choices = data.get('questions')[1].get('choices')
        for index in range(0, 3):
            assert test_choices[index] == choices[index], (
                'Проверьте, что при GET запросе `/api/polls/{poll_id}/` возвращаете данные объекта. '
                'Значение `choices` `questions` неправильное.'
            )

        data = {
            "is_active": False,
            "end_date": datetime.date.today(),
            "title": "Замененный опрос",
            "description": "Описание замененного опроса"
        }

        response = admin_client.patch(
            f'/api/polls/{polls[0]["id"]}/',
            data=data)
        assert response.status_code == 200, (
            'Проверьте, что при PATCH запросе `/api/polls/{poll_id}/` возвращается статус 200'
        )
