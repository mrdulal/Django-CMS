from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    # Public views
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('page/<slug:slug>/', views.PageDetailView.as_view(), name='page_detail'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('search/', views.search_posts, name='search'),
    
    # Comment functionality
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    
    # Admin/Dashboard views
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/post/create/', views.create_post, name='create_post'),
    path('dashboard/post/<slug:slug>/edit/', views.edit_post, name='edit_post'),
    path('dashboard/page/create/', views.create_page, name='create_page'),
]