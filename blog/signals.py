from django.conf import settings
from django.db.models.signals import pre_save

from .models import Comment
from .tasks import send_email

def notify_user_when_comment_published(sender, instance, **kwargs):
   if instance.id is None:
      pass
   else:
      previous = Comment.objects.get(id=instance.id)
      if previous.is_published != instance.is_published:
         if instance.is_published:
            post = instance.post
            author_email = post.author.email
            if settings.DEBUG:
               email_text = f'You received new comment! Check it {post.get_post_url()}'
               send_email.delay('New test comment created!', email_text, author_email)

pre_save.connect(notify_user_when_comment_published, sender=Comment)