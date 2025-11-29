# Make the send email function here
# The import 'from .utils import EMAIL_FUNCTION_NAME in views.py
# This is the Std. way of doing stuff.
# 'utils.py' is for helper functions.
# ---- MAKE NOTES ----

from django.core.mail import send_mail
from django.conf import settings

def send_email_for_verification(message,recipent_email):
    subject ="SUBJECT"
    message=f"Your verification code is: {message}"
    from_email = settings.EMAIL_HOST_USER
    recipent_email= [recipent_email]
    send_mail(subject, message, from_email, recipent_email)