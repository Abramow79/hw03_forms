from django import forms

from .models import Post


""" class CommentForm(forms.ModelForm):
    #Класс для создания формы комментария

    class Meta:
        model = Comment
        fields = ('text',) """


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {'text': 'Текст поста', 'group': 'Выберите группу'}
        help_texts = {
            'text': 'Текст нового поста',
            'group': 'Группа, к которой будет относиться посты'
        }
