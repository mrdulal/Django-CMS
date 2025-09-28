from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'categories', api_views.CategoryViewSet)
router.register(r'posts', api_views.PostViewSet)
router.register(r'pages', api_views.PageViewSet)
router.register(r'comments', api_views.CommentViewSet)
router.register(r'users', api_views.UserViewSet)
router.register(r'settings', api_views.SiteSettingsViewSet)
router.register(r'dashboard', api_views.DashboardViewSet, basename='dashboard')

app_name = 'api'

urlpatterns = [
    # API endpoints
    path('', include(router.urls)),
    
    # API Authentication
    path('auth/', include('rest_framework.urls')),
]