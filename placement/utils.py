# Make the send email function here
# The import 'from .utils import EMAIL_FUNCTION_NAME in views.py
# This is the Std. way of doing stuff.
# 'utils.py' is for helper functions.
# ---- MAKE NOTES ----

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def send_email_for_verification(otp, name,recipent_email):
    subject ="[Samatrix] Code for Email Verification"
    html_message = render_to_string('email_template.html', {'otp': otp, 'name': name})
    message=f"Your verification code is: {otp}"
    from_email = settings.EMAIL_HOST_USER
    recipent_email= [recipent_email]
    send_mail(subject, message, from_email, recipent_email, html_message=html_message)