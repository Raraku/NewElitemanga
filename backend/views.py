from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.views.decorators.vary import vary_on_cookie
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from users.models import Profile, User
from rest_auth.registration.views import SocialConnectView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from allauth.account.models import EmailAddress
from django.contrib import messages
from allauth.account.adapter import get_adapter


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


# Create your views here.


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def verify_email(request):
    subject = "EliteManga - Email Registration"
    message = "Thank you for signing up to EliteManga, we are really happy you have decided to join us on this journey. Dōmo arigatōgozaimashita"
    email_from = "noreply@elitemanga.net"
    recipient_list = [
        "joas592@gmail.com",
    ]
    send_mail(subject, message, email_from, recipient_list)
    return Response(status=status.HTTP_200_OK)


@api_view(["get"])
def action_send(request):
    email = request.user.email
    print(email)
    try:
        email_address = EmailAddress.objects.get(user=request.user, email=email,)
        get_adapter(request).add_message(
            request,
            messages.INFO,
            "account/messages/" "email_confirmation_sent.txt",
            {"email": email},
        )
        email_address.send_confirmation(request)

        return Response(status=status.HTTP_200_OK)
    except Exception as exc:
        return Response(status=status.HTTP_400_BAD_REQUEST)
