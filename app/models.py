from django.db import models

from django.contrib.auth.models import AbstractUser
from djstripe.utils import subscriber_has_active_subscription

from django.utils.functional import cached_property

# Create your models here.


class Organization(models.Model):
    name = models.TextField()

    @property
    def email(self):
        return self.users.first().email

    @property
    def customer(self):
        return self.djstripe_customers.first()

    @property
    def has_active_subscription(self):
        return subscriber_has_active_subscription(self)

    @property
    def has_incomplete_subscription(self):
        return len(self.customer.subscriptions.filter(status="incomplete")) > 0

    def __str__(self):
        return self.name


class User(AbstractUser):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True,
    )

    @property
    def has_active_subscription(self):
        return self.organization.has_active_subscription

    @property
    def has_incomplete_subscription(self):
        return self.organization.has_incomplete_subscription
