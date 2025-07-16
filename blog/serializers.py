from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment, Category, Subscription, CommentReaction
from django.contrib.auth import get_user_model

User = get_user_model()
# Получаем кастомную модель пользователя
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar', 'bio']  # Поля модели UserProfile

class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели категории."""
    class Meta:
        model = Category
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели постов."""
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели комментариев."""
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

class CommentReactionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели реакций на комментарии."""
    user = UserSerializer(read_only=True)

    class Meta:
        model = CommentReaction
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели подписок."""
    follower = UserSerializer(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = '__all__'
