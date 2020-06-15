from django.contrib import admin
import app.models as models

# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Organization)
