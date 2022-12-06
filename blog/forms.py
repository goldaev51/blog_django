from django.forms import ModelForm

from .models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'short_description', 'description', 'image_field', 'is_active']
