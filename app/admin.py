from django.contrib import admin

from .models import Comment, Level, Like, Post, Ask, Question

admin.site.register(Level),
admin.site.register(Post),
admin.site.register(Ask),
admin.site.register(Question)
admin.site.register(Comment)
admin.site.register(Like)
