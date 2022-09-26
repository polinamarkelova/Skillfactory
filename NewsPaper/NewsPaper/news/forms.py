from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Author


class PostForm(forms.ModelForm):
    title = forms.CharField(min_length=10)

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'category',
            'author',
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if title == text:
            raise ValidationError(
                "Заголовок не должно быть идентичен тексту статьи."
            )
        return cleaned_data


