from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib import messages, auth
from accounts.models import Token
from django.urls import reverse
from accounts.authentication import PasswordlessAuthenticationBackend

def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + '?token={uid}'.format(uid=str(token.uid))
    )
    message_body = 'Use this link to log in:\n\n{url}'.format(url=url)
    send_mail(
        'Your login link for Superlists',
        message_body,
        'noreply@superlists',
        [email]
    )
    messages.success(
        request,
        "Check your email, we've sent you a link you can use to log in."
    )
    return redirect('/')

def login(request):
    token_uid = request.GET.get('token')
    user = PasswordlessAuthenticationBackend().authenticate(token_uid)
    if user:
        auth.login(request, user)
    return redirect('/')
