from django.contrib.auth import get_user_model
from django import forms

from .models import Post, Comment

User = get_user_model()


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group', 'image', ]


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'post']
