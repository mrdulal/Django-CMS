from django.contrib import admin
from django.contrib.admin import AdminSite
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from cms.models import Post, Comment, Category, Page
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta


class CustomAdminSite(AdminSite):
    site_title = 'Django CMS Admin'
    site_header = 'Django CMS Administration'
    index_title = 'Welcome to Django CMS Admin Panel'
    
    @method_decorator(never_cache)
    @method_decorator(staff_member_required)
    def index(self, request, extra_context=None):
        """
        Display the main admin index page with dashboard statistics.
        """
        # Get statistics
        total_posts = Post.objects.count()
        published_posts = Post.objects.filter(status='published').count()
        draft_posts = Post.objects.filter(status='draft').count()
        total_comments = Comment.objects.count()
        pending_comments = Comment.objects.filter(is_approved=False).count()
        total_categories = Category.objects.count()
        total_pages = Page.objects.count()
        
        # Get recent posts
        recent_posts = Post.objects.select_related('author', 'category').order_by('-created_at')[:5]
        
        # Get recent comments
        recent_comments = Comment.objects.select_related('post').order_by('-created_at')[:5]
        
        # Get posts by month for chart data
        now = timezone.now()
        monthly_data = []
        monthly_labels = []
        
        for i in range(6):
            month_start = now.replace(day=1) - timedelta(days=30 * i)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            posts_count = Post.objects.filter(
                created_at__gte=month_start,
                created_at__lte=month_end
            ).count()
            monthly_data.insert(0, posts_count)
            monthly_labels.insert(0, month_start.strftime('%b'))
        
        # Category distribution
        category_data = Category.objects.annotate(
            post_count=Count('posts')
        ).order_by('-post_count')[:5]
        
        context = {
            'total_posts': total_posts,
            'published_posts': published_posts,
            'draft_posts': draft_posts,
            'total_comments': total_comments,
            'pending_comments': pending_comments,
            'total_categories': total_categories,
            'total_pages': total_pages,
            'recent_posts': recent_posts,
            'recent_comments': recent_comments,
            'monthly_data': monthly_data,
            'monthly_labels': monthly_labels,
            'category_data': category_data,
        }
        
        if extra_context:
            context.update(extra_context)
            
        return super().index(request, context)


# Create custom admin site instance
custom_admin_site = CustomAdminSite(name='custom_admin')