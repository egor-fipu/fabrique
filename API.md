## Для администратора системы

### Создание опроса
POST-запрос на адрес /api/polls/
```
{
    "is_active": true,
    "title": "Первый опрос",
    "description": "Описание первого опроса"
}
```
*по адресу /api/polls/<poll_id>/ также доступно*
- *изменение, удаление, замена опроса*
### Получение списка опросов
GET-запрос на адрес /api/polls/
```
[
    {
        "id": 1,
        "is_active": true,
        "start_date": "yyyy-mm-dd",
        "end_date": null,
        "title": "Первый опрос",
        "description": "Описание первого опроса"
    },
    ...
]
```

### Получение подробной информации об опросе
GET-запрос на адрес /api/polls/<poll_id>/
```
{
    "id": 1,
    "is_active": true,
    "start_date": "yyyy-mm-dd",
    "end_date": null,
    "title": "Первый опрос",
    "description": "Описание первого опроса",
    "questions": [
        {
            "id": 1,
            "type": "Text",
            "text": "Первый вопрос",
            "choices": []
        },
        {
            "id": 2,
            "type": "Many_choices",
            "text": "Второй вопрос",
            "choices": [
                {
                    "id": 1,
                    "text": "Первый вариант ответа"
                },
                {
                    "id": 2,
                    "text": "Второй вариант ответа"
                },
                {
                    "id": 3,
                    "text": "Третий вариант ответа"
                }
            ]
        },
        ...
    ]
}
```

### Создание вопроса в опросе
POST-запрос на адрес /api/polls/<poll_id>/questions/
```
{
    "type": "One_choice",
    "text": "Первый вопрос",
    "choices": [
        {
            "text": "Первый вариант ответа"
        },
        {
            "text": "Второй вариант ответа"
        },
        {
            "text": "Третий вариант ответа"
        }
    ]
}
```
*по адресу /api/polls/<poll_id>/questions/<question_id>/ также доступно*
- *получение подробной информации о вопросе*
- *удаление вопроса*
- *изменение, замена полей "type" и "text" вопроса*

### Варианты ответов в вопросе
*по адресу /api/polls/<poll_id>/questions/<question_id>/choices/ доступно*
- *просмотр списка вариантов ответа в вопросе*

*по адресу /api/polls/<poll_id>/questions/<question_id>/choices/<choice_id>/ доступно*
- *просмотр, замена, изменение, удаление варианта ответа в вопросе*

## Для пользователя (в том числе анонимного)
### Получение списка опросов
GET-запрос на адрес /api/users/polls/
```
[
    {
        "id": 1,
        "title": "Первый опрос",
        "description": "Описание первого опроса"
    },
    ...
]
```

### Получение подробной информации об опросе
GET-запрос на адрес /api/users/polls/<poll_id>/
```
{
    "id": 1,
    "title": "Первый опрос",
    "description": "Описание первого опроса",
    "questions": [
        {
            "id": 1,
            "type": "Text",
            "text": "Первый вопрос",
            "choices": []
        },
        {
            "id": 2,
            "type": "Many_choices",
            "text": "Второй вопрос",
            "choices": [
                {
                    "id": 1,
                    "text": "Первый вариант ответа"
                },
                {
                    "id": 2,
                    "text": "Второй вариант ответа"
                },
                {
                    "id": 3,
                    "text": "Третий вариант ответа"
                }
            ]
        },
        ...
    ]
}
```

### Прохождение опроса
POST-запрос на адрес /api/users/tests/
```
{
    "id_user": 111,
    "poll": <poll_id>,
    "answers": [
        {
            "question": <question_id>,
            "text": "Ответ"
        },
        {
            "question": <question_id>,
            "choice_id": [<choice_id>,<choice_id>]
        },
        {
            "question": <question_id>,
            "choice_id": [<choice_id>]
        },
        ...
    ]
}
```

### Получение пройденных пользователем опросов
GET-запрос на адрес /api/users/tests/?user=<id_user>
```
[
    {
        "user": null,
        "id_user": <id_user>,
        "poll": "Первый опрос",
        "created": "dd.mm.yyyy",
        "answers": [
            {
                "question": "Первый вопрос (Text)",
                "choice": [],
                "text": "Ответ"
            },
            {
                "question": "Второй вопрос (Many_choices)",
                "choice": [
                    "id:1, Первый вариант ответа",
                    "id:2, Второй вариант ответа"
                ],
                "text": null
            },
            {
                "question": "Третий вопрос (One_choice)",
                "choice": [
                    "id:4, Первый вариант ответа"
                ],
                "text": null
            },
            ...
        ]
    }
]
```