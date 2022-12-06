from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (CommentViewSet, ReviewViewSet, UsersViewSet,
                    signup, get_token)
from api import views

router_v1 = DefaultRouter()
router_v1.register('titles', views.TitlesViewSet, basename='titles')
router_v1.register(
    r'categories',
    views.CategoriesViewSet, basename='categories'
)
router_v1.register('genres', views.GenresViewSet, basename='genres')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                   r'/comments', CommentViewSet, basename='comments')
router_v1.register('users', UsersViewSet, basename='users')

auth_path = [
    path('auth/signup/', signup),
    path('auth/token/', get_token)
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include(auth_path))
]
