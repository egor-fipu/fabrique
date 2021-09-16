import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


class Test00UserAuth:
    url_token = '/auth/jwt/create/'

    @pytest.mark.django_db(transaction=True)
    def test_00_obtain_jwt_token_invalid_data(self, client):
        request_type = 'POST'
        response = client.post(self.url_token)
        assert response.status_code != 404, (
            f'Страница `{self.url_token}` не найдена, проверьте этот адрес в *urls.py*'
        )

        code = 400
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе `{self.url_token}` без параметров, '
            f'возвращается статус {code}'
        )

        invalid_data = {
            'password': 1234567
        }
        response = client.post(self.url_token, data=invalid_data)
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе `{self.url_token}` без username, '
            f'возвращается статус {code}'
        )

        invalid_data = {
            'username': 'unexisting_user',
            'password': 1234567
        }
        response = client.post(self.url_token, data=invalid_data)
        code = 401
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе `{self.url_token}` с несуществующим username, '
            f'возвращается статус {code}'
        )

        invalid_data = {
            'username': 'TestSuperuser',
            'password': 123456
        }
        response = client.post(self.url_token, data=invalid_data)
        code = 401
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе `{self.url_token}` с валидным username, '
            f'но невалидным password, возвращается статус {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_00_obtain_jwt_token_valid_data(self, client, admin):
        request_type = 'POST'

        valid_username = 'TestSuperuser'
        valid_password = 1234567

        valid_data = {
            'password': valid_password,
            'username': valid_username
        }
        response = client.post(self.url_token, data=valid_data)
        code = 200
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе `{self.url_token}` с валидными данными '
            f'генерируется токен и возвращается статус {code}'
        )

        assert "access" in response.json(), (
            f'Проверьте, что при {request_type} запросе `{self.url_token}` с валидными данными '
            f'в ответе возвращается токен в поле "access"'
        )

        assert "refresh" in response.json(), (
            f'Проверьте, что при {request_type} запросе `{self.url_token}` с валидными данными '
            f'в ответе возвращается refresh-токен в поле "refresh"'
        )
