from django.contrib import admin

from .models import Poll, Question, Choice, Answer, Test


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'description')
    empty_value_display = '-пусто-'


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('user', 'id_user', 'poll', 'created')
    empty_value_display = '-пусто-'


admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Answer)
