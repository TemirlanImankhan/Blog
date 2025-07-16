from django.contrib import admin
from .models import UserProfile, Post, Comment, Category, Subscription, CommentReaction

# Регистрация моделей в админке
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Subscription)
admin.site.register(CommentReaction)

# Register your models here.
