from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import UsersViewSet, signup, get_token

app_name = 'api'

router = DefaultRouter()

router.register('users', UsersViewSet, basename='users')

urlpatterns = [path('v1/', include(router.urls)),
               path('v1/auth/signup/', signup),
               path('v1/auth/token/', get_token),
               ]
