from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from rest_framework import viewsets, permissions, serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment, Category, Subscription, CommentReaction, UserProfile
from .forms import PostForm, EditProfileForm, CustomUserCreationForm
from .serializers import PostSerializer, CommentSerializer, CategorySerializer, SubscriptionSerializer, CommentReactionSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Post, Comment, Category, Subscription
from .forms import PostForm, EditProfileForm, CustomUserCreationForm
from django.shortcuts import get_object_or_404, redirect
from .models import Post
from django.http import JsonResponse

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        post.delete()
    return redirect('profile')

User = get_user_model()
User = get_user_model()
User = get_user_model()

# Главная страница
def home(request):
    posts = Post.objects.all()  # Получаем все посты
    return render(request, 'blog/index.html', {'posts': posts})

# Детали поста
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})

# Создание поста
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # Не сохраняем в базу сразу
            post.author = request.user  # Устанавливаем текущего пользователя как автора
            post.save()  # Сохраняем пост в базу
            return redirect('home')  # Перенаправляем на главную страницу
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

# Редактирование поста
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})

# Удаление поста
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('profile')
    return render(request, 'blog/delete_post.html', {'post': post})

# Профиль пользователя
@login_required
def profile(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/profile.html', {'posts': posts})

# Редактирование профиля
from django.shortcuts import render, redirect
from .forms import EditProfileForm
from django.contrib.auth.decorators import login_required

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Перенаправление на страницу профиля
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'blog/edit_profile.html', {'form': form})

# Добавление комментария
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, user=request.user, content=content)
        return redirect('post_detail', post_id=post.id)
    return redirect('home')

# Поиск постов
from django.shortcuts import render
from .models import Post

def search_posts(request):
    query = request.GET.get('q', '').strip()  # Получаем поисковый запрос (может быть пустым)
    category_id = request.GET.get('category')  # Получаем выбранную категорию
    posts = Post.objects.all()

    # Фильтрация по запросу
    if query:
        posts = posts.filter(title__icontains=query)

    # Фильтрация по категории
    if category_id:
        posts = posts.filter(category_id=category_id)

    categories = Category.objects.all()  # Получаем все категории
    return render(request, 'blog/search_results.html', {
        'posts': posts,
        'categories': categories,
        'query': query,
        'selected_category': category_id,  # Для сохранения выбранной категории
    })

# Регистрация пользователя
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

from .forms import CustomUserCreationForm

def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

# Логин пользователя
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'blog/login.html', {'error': 'Неверный логин или пароль'})
    return render(request, 'blog/login.html')

# Логаут пользователя
def user_logout(request):
    logout(request)
    return redirect('home')

# API ViewSets
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        author = self.request.data.get('author')
        if self.request.user.id == int(author):
            raise serializers.ValidationError("Нельзя подписаться на самого себя.")
        serializer.save(follower=self.request.user)

class CommentReactionViewSet(viewsets.ModelViewSet):
    queryset = CommentReaction.objects.all()
    serializer_class = CommentReactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@login_required
def like_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
            post.dislikes.remove(request.user)
        return JsonResponse({'likes_count': post.likes.count(), 'dislikes_count': post.dislikes.count()})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def dislike_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        if request.user in post.dislikes.all():
            post.dislikes.remove(request.user)
        else:
            post.dislikes.add(request.user)
            post.likes.remove(request.user)
        return JsonResponse({'likes_count': post.likes.count(), 'dislikes_count': post.dislikes.count()})
    return JsonResponse({'error': 'Invalid request'}, status=400)

from django.shortcuts import render
from .models import Post, Category

def index(request):
    query = request.GET.get('q')  # Получаем поисковый запрос
    category_id = request.GET.get('category')  # Получаем выбранную категорию
    tags = request.GET.get('tags')  # Получаем теги
    posts = Post.objects.all()

    # Фильтрация по запросу
    if query:
        posts = posts.filter(title__icontains=query)

    # Фильтрация по категории
    if category_id:
        posts = posts.filter(category_id=category_id)

    # Фильтрация по тегам
    if tags:
        tag_list = [tag.strip() for tag in tags.split(',')]
        posts = posts.filter(tags__name__in=tag_list).distinct()

    categories = Category.objects.all()  # Получаем все категории
    return render(request, 'blog/index.html', {
        'posts': posts,
        'categories': categories,
        'query': query,
    })
