# Create your tasks here
from celery import shared_task

from django.core.mail import send_mail


@shared_task
def send_email_comment(email_subject, email_body, email_to):
    send_mail(
        email_subject,
        email_body,
        'no-reply@admin.com',
        [email_to],
        fail_silently=False,
    )
