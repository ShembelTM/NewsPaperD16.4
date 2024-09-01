from .models import Post, Category
from django import forms
from django.core.exceptions import ValidationError


class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'text',
            'categoryType',
        ]
        labels = {
            'author': 'Автор',
            'title': 'Заголовок',
            'text': 'Текст',
            'categoryType': 'Категории'
        }

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get('text')
        name = cleaned_data.get('title')
        if name == description:
            raise ValidationError('Текст не должен совпадать с заголовком')
        return cleaned_data