from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # re_path(
    #     r"^email-verification/$",
    #     TemplateView.as_view(template_name="email_verification.html"),
    #     name="email-verification",
    # ),
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
    # path(
    #     r"^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
    #     TemplateView.as_view(template_name="password_reset_confirm.html"),
    #     name="password_reset_confirm",
    # ),
    path("api-auth/", include("rest_framework.urls")),
    path("accounts/", include("allauth.urls")),
    path("rest-auth/", include("rest_auth.urls")),
    path("rest-auth/registration/", include("rest_auth.registration.urls")),
    path("admin/", admin.site.urls),
    path("", include("backend.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
