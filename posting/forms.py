from django import forms
from django.forms import ModelChoiceField
from .models import Question, Answer, Comment, Category


class CategoryChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        # return '{}: {}'.format(obj.id, obj.name)
        return '{}'.format(obj.name)


class QuestionForm(forms.ModelForm):

    category = CategoryChoiceField(widget=forms.Select, queryset=Category.objects.all(), required=True)
    class Meta:
        model = Question
        fields = ['category', 'subject', 'content']
        labels = {
            'subject': '제목',
            'category': '구분',
            'content': '내용',
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '내용',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_content']
        label = {
            'comment_content': '댓글내용',
        }


#
# class SortForm(forms.Form):
#     sort = forms.ChoiceField(choices=[(x, x) for x in ['recent', 'recommend', 'popular']])
