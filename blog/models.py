from django.conf import settings
from django.db import models
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=300)
    short_description = models.TextField()
    description = models.TextField()
    image_field = models.ImageField(blank=True, null=True, upload_to='post_images')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('blog:post-detail', args=[str(self.id)])


class Comment(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
