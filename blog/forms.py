from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'short_description', 'description', 'image_field', 'is_active']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['username', 'text']
