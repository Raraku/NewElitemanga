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
