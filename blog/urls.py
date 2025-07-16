from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    index,  # Убедитесь, что index импортирован
    PostViewSet, CommentViewSet, CategoryViewSet,
    SubscriptionViewSet, CommentReactionViewSet,
    post_detail, user_login, user_logout,
    user_register, profile, create_post, edit_post,
    add_comment, edit_profile, search_posts, delete_post, like_post, dislike_post
)

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'reactions', CommentReactionViewSet)

urlpatterns = [
    # HTML маршруты
    path('', index, name='home'),  # Убедитесь, что index используется
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),
    path('profile/', profile, name='profile'),
    path('create/', create_post, name='create_post'),
    path('post/edit/<int:post_id>/', edit_post, name='edit_post'),
    path('post/<int:post_id>/add_comment/', add_comment, name='add_comment'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('search/', search_posts, name='search_posts'),
    path('accounts/', include('allauth.urls')),
    path('like/<int:post_id>/', like_post, name='like_post'),
    path('dislike/<int:post_id>/', dislike_post, name='dislike_post'),
    path('delete/<int:post_id>/', delete_post, name='delete_post'),

    # API маршруты
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


