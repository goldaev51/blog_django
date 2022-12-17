# Create your tasks here
from celery import shared_task

from django.core.mail import send_mail


@shared_task
def send_email(email_subject, email_body, email_to):
    send_mail(
        email_subject,
        email_body,
        'no-reply@admin.com',
        [email_to],
        fail_silently=False,
    )


@shared_task
def send_feedback_email(email_body, email_from):
    send_mail(
        'New feedback received',
        email_body,
        email_from,
        ['admin@admin.com'],
        fail_silently=False,
    )
