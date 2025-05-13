from django.core.mail import send_mail
import random

def generate_verification_code():
    return str(random.randint(100000, 999999))

def send_verification_email(email, code):
    send_mail(
        subject='Email Tasdiqlash Kodingiz',
        message=f"Sizning tasdiqlash kodingiz: {code}",
        from_email='noreply@financeapp.uz',
        recipient_list=[email],
        fail_silently=False
    )
