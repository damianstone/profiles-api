from django.urls import path, include

from rest_framework.routers import DefaultRouter

from profiles_api import views

# implement url for viewSets
router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')
# if u are usingn a queryset so not use base_name
router.register('profile', views.ProfileViewSet)
router.register('feed', views.UserProfileFeedViewSet)

urlpatterns = [
    path('hello-view/', views.HelloApi.as_view()),
    path('login/', views.UserLoginApiView.as_view()),
    path('', include(router.urls))
]
