import sys
from django.urls import include, path
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

from . import views

from djstripe import webhooks


@webhooks.handler("customer.created")
def my_handler(event, **kwargs):
    print("\n\n\nWebhook triggered\n\n\n")


urlpatterns = [
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
    path("create-checkout-session/", views.CreateCheckoutAPIView.as_view()),
    path(
        "subscriptions-list/",
        TemplateView.as_view(template_name="subscription-list.html"),
    ),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", views.MyRegistrationView.as_view(), name="register"),
    path("home/", views.HomeView.as_view(), name="home"),
]
