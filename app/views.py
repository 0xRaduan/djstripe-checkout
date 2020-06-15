from django.shortcuts import render
from django.conf import settings
from django.views.generic.edit import CreateView
from django.views import View
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from djstripe.models import Customer
from app.forms import RegForm
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from app.models import User

import stripe

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

# Create your views here.


class CreateCheckoutAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        print("something happens")
        plan_id = request.data.get("planId")
        current_user = User.objects.last()
        if current_user.has_active_subscription:  # check plans instead
            return Response({"message": "User already have subscription!"})
        kwargs = {
            "success_url": "",
            "cancel_url": "",
            "mode": "subscription",
            "payment_method_types": ["card"],
            "line_items": [{"price": plan_id, "quantity": 1}],
            "customer": current_user.organization.djstripe_customers.first().id,
        }
        checkout = stripe.checkout.Session.create(**kwargs)
        return Response({"sessionId": checkout["id"]})


class MyRegistrationView(CreateView):
    form_class = RegForm
    template_name = "registration.html"
    success_url = reverse_lazy("login")


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        user = self.request.user
        if not user.has_active_subscription:
            return HttpResponse(
                f"Seems, like you are on a free plan in {user.organization} organization"
            )
        subscription = (
            user.organization.djstripe_customers.all()
            .first()
            .subscriptions.all()
            .first()
        )
        plan = subscription.plan
        return HttpResponse(
            f"You have {plan.nickname} plan in {user.organization} organization"
        )
