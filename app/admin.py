from django.contrib import admin
from .models import Level, Post,Ask,Question

admin.site.register(Post)
admin.site.register(Ask)
admin.site.register(Question)
admin.site.register(Level)
