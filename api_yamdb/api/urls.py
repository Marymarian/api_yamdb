from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import UsersViewSet

app_name = 'api'

router = DefaultRouter()

router.register('users', UsersViewSet, basename='users')

urlpatterns = [path('v1/', include(router.urls))]
