from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=300)
    short_description = models.TextField()
    description = models.TextField()
    image_field = models.ImageField(blank=True, null=True, upload_to='post_images')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    pubdate = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('blog:post-detail', args=[str(self.id)])


    def get_admin_post_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse(f"admin:{content_type.app_label}_{content_type.model}_change", args=(self.id,))


    def get_post_url(self):
        return reverse(f"blog:post-detail", args=(self.id,))


    class Meta:
        ordering = ('-pubdate',)


class Comment(models.Model):
    # username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments', null=True)
    username = models.CharField(max_length=100)
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    pubdate = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=False)

    def publish_comment(self):
        self.is_published = True
        self.save()

    def get_admin_comment_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse(f"admin:{content_type.app_label}_{content_type.model}_change", args=(self.id,))


    class Meta:
        ordering = ('-pubdate',)
