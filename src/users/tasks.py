import uuid

from django.core.mail import send_mail

from config import celery_app


@celery_app.task
def send_activation_mail(recipient: str, activation_link: uuid.UUID):
    send_mail(
        subject="Activate your account",
        message=f"Please click the following link to activate your account: {activation_link}",
        from_email="admin@support.com",
        recipient_list=[recipient],
    )
