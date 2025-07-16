from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post, UserProfile

class CustomUserCreationForm(UserCreationForm):
    """Кастомная форма для регистрации пользователя."""
    class Meta:
        model = UserProfile  # Используем вашу кастомную модель пользователя
        fields = ['username', 'email', 'password1', 'password2', 'avatar', 'bio']

class EditProfileForm(forms.ModelForm):
    """Форма для редактирования профиля пользователя."""
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio']  # Поля для редактирования профиля

class PostForm(forms.ModelForm):
    """Форма для создания и редактирования постов."""
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image']  # Добавлено поле image

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio']
