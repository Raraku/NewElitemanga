from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from allauth.account.views import confirm_email
from backend.views import GoogleLogin, FacebookLogin, action_send

urlpatterns = [
    # path(
    #     r"^password-reset/$",
    #     TemplateView.as_view(template_name="password_reset.html"),
    #     name="password-reset",
    # ),
    # path(
    #     r"^password-reset/confirm/$",
    #     TemplateView.as_view(template_name="password_reset_confirm.html"),
    #     name="password-reset-confirm",
    # ),
    path("verify-email/", action_send, name="account_email"),
    # path(
    #     r"^user-details/$",
    #     TemplateView.as_view(template_name="user_details.html"),
    #     name="user-details",
    # ),
    # path(
    #     r"^password-change/$",
    #     TemplateView.as_view(template_name="password_change.html"),
    #     name="password-change",
    # ),
    # # this path is used to generate email content
    url(
        r"^rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$",
        confirm_email,
        name="account_confirm_email",
    ),
    # path(
    #     r"^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
    #     TemplateView.as_view(template_name="password_reset_confirm.html"),
    #     name="password_reset_confirm",
    # ),
    path("api-auth/", include("rest_framework.urls")),
    path("accounts/", include("allauth.urls")),
    path("rest-auth/", include("rest_auth.urls")),
    path("summernote/", include("django_summernote.urls")),
    path("rest-auth/facebook/", FacebookLogin.as_view(), name="fb_login"),
    path("rest-auth/google/", GoogleLogin.as_view(), name="google_login"),
    path("rest-auth/registration/", include("rest_auth.registration.urls")),
    path("admin/", admin.site.urls),
    path("", include("backend.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
