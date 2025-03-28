from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from celery import shared_task


@shared_task
def send_email_to_user(subject: str, email: str, message: str):
    """
    This method sends an email to a user using Django's EmailMultiAlternatives.
    It is decorated with @shared_task to be used as a Celery task.

    Args:
        subject (str): The subject of the email.
        email (str): The recipient's email address.
        message (str): The HTML content of the email.
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    # Create email message with HTML alternative
    email_message = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=from_email,
        to=recipient_list
    )

    # Attach HTML content with proper MIME type
    email_message.attach_alternative(message, "text/html")

    # Send the email
    email_message.send()