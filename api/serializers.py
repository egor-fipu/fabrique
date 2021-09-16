from rest_framework import serializers

from .fields import ChoiceIdField
from .models import Poll, Question, Choice, Answer, Test, ChoiceAnswer


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'text')

    def validate(self, data):
        question_id = self.context['view'].kwargs['question_id']
        question = Question.objects.get(id=question_id)
        if question.type == 'Text':
            raise serializers.ValidationError(
                'В вопросе с типом "Text" не может быть вариантов ответа!'
            )
        return data


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ('id', 'type', 'text', 'choices')

    def create(self, validated_data):
        if 'choices' in validated_data:
            choices = validated_data.pop('choices')
            question = Question.objects.create(**validated_data)
            for choice in choices:
                Choice.objects.create(**choice, question=question)
            return question
        else:
            question = Question.objects.create(**validated_data)
            return question

    def validate_choices(self, value):
        if self.initial_data['type'] == 'Text' and value.__len__ != 0:
            raise serializers.ValidationError(
                'В вопросе с типом "Text" не может быть вариантов ответа!'
            )
        return value


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        model = Poll
        fields = (
            'id',
            'is_active',
            'start_date',
            'end_date',
            'title',
            'description',
            'questions'
        )
        read_only_fields = ('start_date',)

    def create(self, validated_data):
        if 'questions' in validated_data:
            questions = validated_data.pop('questions')
            poll = Poll.objects.create(**validated_data)
            for question in questions:
                Question.objects.create(**question, poll=poll)
            return poll
        else:
            poll = Poll.objects.create(**validated_data)
            return poll

    def validate_end_date(self, value):
        if self.instance and value < self.instance.start_date:
            raise serializers.ValidationError(
                'Дата окончания не может быть ранее даты начала'
            )
        return value


class PollListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = (
            'id',
            'is_active',
            'start_date',
            'end_date',
            'title',
            'description'
        )


# Для пользователей #


class UserPollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        model = Poll
        fields = ('id', 'title', 'description', 'questions')


class UserPollListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ('id', 'title', 'description')


class UserAnswerSerializer(serializers.ModelSerializer):
    choice_id = ChoiceIdField(
        queryset=Choice.objects.all(),
        write_only=True,
        many=True,
        required=False
    )

    class Meta:
        model = Answer
        fields = ('id', 'question', 'choice', 'choice_id', 'text')


class UserTestSerializer(serializers.ModelSerializer):
    answers = UserAnswerSerializer(
        many=True,
    )

    class Meta:
        model = Test
        fields = ('id', 'id_user', 'poll', 'answers')

    def validate_answers(self, value):
        for answer in value:
            if answer['question'].type == 'Text' and ('choice_id' in answer):
                raise serializers.ValidationError(
                    f'В вопросе id {answer["question"].id} с типом "Text" не '
                    f'может быть вариантов ответа!'
                )
            if answer['question'].type == 'Text' and ('text' not in answer):
                raise serializers.ValidationError(
                    f'В вопросе id {answer["question"].id} с типом "Text" '
                    f'введите текст ответа!'
                )
            if ((answer['question'].type == 'One_choice'
                 or answer['question'].type == 'Many_choices')
                    and ('choice_id' not in answer)):
                raise serializers.ValidationError(
                    f'В вопросе id {answer["question"].id} с типом '
                    f'{answer["question"].type} должны быть варианты ответа!'
                )
            if (answer['question'].type == 'One_choice'
                    and len(answer['choice_id']) != 1):
                raise serializers.ValidationError(
                    f'В вопросе id {answer["question"].id} с типом '
                    f'"One_choice" должен быть один вариант ответа!'
                )
            if (answer['question'].type == 'Many_choices'
                    and len(answer['choice_id']) < 2):
                raise serializers.ValidationError(
                    f'В вопросе id {answer["question"].id} с типом '
                    f'"Many_choices" должно быть больше одного варианта ответа!'
                )
            if ((answer['question'].type == 'One_choice'
                 or answer['question'].type == 'Many_choices')
                    and ('text' in answer)):
                raise serializers.ValidationError(
                    f'В вопросе id {answer["question"].id} с типом '
                    f'{answer["question"].type} не может быть текстового '
                    f'ответа!'
                )
        return value

    def create(self, validated_data):
        if 'answers' not in validated_data:
            raise serializers.ValidationError(
                'Введите ответы на вопросы'
            )
        answers = validated_data.pop('answers')
        test = Test.objects.create(**validated_data)
        for answer in answers:
            if 'choice_id' in answer:
                choice_id = answer.pop('choice_id')
                answer = Answer.objects.create(**answer, test=test)
                for pk in choice_id:
                    ChoiceAnswer.objects.create(choice_id=pk, answer=answer)
            else:
                Answer.objects.create(**answer, test=test)

        return test


class UserTestViewAnswersSerializer(serializers.ModelSerializer):
    question = serializers.StringRelatedField()
    choice = serializers.StringRelatedField(many=True)

    class Meta:
        model = Answer
        fields = ('question', 'choice', 'text')


class UserTestViewSerializer(serializers.ModelSerializer):
    answers = UserTestViewAnswersSerializer(many=True)
    poll = serializers.StringRelatedField()
    created = serializers.DateTimeField(format='%d.%m.%Y')

    class Meta:
        model = Test
        fields = ('user', 'id_user', 'poll', 'created', 'answers')
