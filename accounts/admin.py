from django.contrib import admin

from .models import CustomUser, Ocupation

admin.site.register(CustomUser)
admin.site.register(Ocupation)