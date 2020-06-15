from app.models import User, Organization
from django.contrib.auth.forms import UserCreationForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.db import transaction

from djstripe.models import Customer


class RegForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Submit"))

    email = forms.EmailField()
    organization = forms.CharField()

    class Meta:
        model = User
        fields = ["email", "username"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        organization, _ = Organization.objects.get_or_create(
            name=self.cleaned_data["organization"]
        )

        user.organization = organization
        user.save()

        _ = Customer.get_or_create(subscriber=organization)
        return user
