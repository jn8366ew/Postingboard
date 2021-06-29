from django.contrib import admin
from .models import Question, Category, Ip


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Category)
admin.site.register(Ip)


