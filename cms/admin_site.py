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
        Display the main admin index page with enhanced dashboard.
        """
        # Get basic statistics
        total_posts = Post.objects.count()
        published_posts = Post.objects.filter(status='published').count()
        draft_posts = Post.objects.filter(status='draft').count()
        total_comments = Comment.objects.count()
        pending_comments = Comment.objects.filter(is_approved=False).count()
        approved_comments = Comment.objects.filter(is_approved=True).count()
        total_categories = Category.objects.count()
        total_pages = Page.objects.count()
        
        # Get recent activity
        recent_posts = Post.objects.select_related('author', 'category').order_by('-created_at')[:8]
        recent_comments = Comment.objects.select_related('post').order_by('-created_at')[:8]
        
        # Get chart data for weekly analytics
        now = timezone.now()
        weekly_data = []
        weekly_labels = []
        
        for i in range(6, -1, -1):
            day_date = now - timedelta(days=i)
            day_start = day_date.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_date.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            posts_count = Post.objects.filter(
                created_at__range=[day_start, day_end]
            ).count()
            
            weekly_data.append(posts_count)
            weekly_labels.append(day_date.strftime('%a'))
        
        # Monthly data for trends
        monthly_data = []
        monthly_labels = []
        
        for i in range(5, -1, -1):
            month_date = now - timedelta(days=i*30)
            month_start = month_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if i == 0:
                month_end = now
            else:
                next_month = month_start.replace(month=month_start.month + 1) if month_start.month < 12 else month_start.replace(year=month_start.year + 1, month=1)
                month_end = next_month - timedelta(days=1)
            
            posts_count = Post.objects.filter(
                created_at__range=[month_start, month_end]
            ).count()
            
            monthly_data.append(posts_count)
            monthly_labels.append(month_date.strftime('%b'))
        
        # Category distribution
        category_data = Category.objects.annotate(
            post_count=Count('posts')
        ).order_by('-post_count')[:5]
        
        # Team/Author stats
        from django.contrib.auth.models import User
        top_authors = User.objects.annotate(
            post_count=Count('posts')
        ).filter(post_count__gt=0).order_by('-post_count')[:4]
        
        context = {
            # Basic stats
            'total_posts': total_posts,
            'published_posts': published_posts,
            'draft_posts': draft_posts,
            'total_comments': total_comments,
            'pending_comments': pending_comments,
            'approved_comments': approved_comments,
            'total_categories': total_categories,
            'total_pages': total_pages,
            
            # Recent activity
            'recent_posts': recent_posts,
            'recent_comments': recent_comments,
            
            # Chart data
            'weekly_data': weekly_data,
            'weekly_labels': weekly_labels,
            'monthly_data': monthly_data,
            'monthly_labels': monthly_labels,
            
            # Analytics
            'category_data': category_data,
            'top_authors': top_authors,
            
            # Additional metrics for dashboard cards
            'engagement_rate': round((total_comments / total_posts * 100) if total_posts > 0 else 0, 1),
            'approval_rate': round((approved_comments / total_comments * 100) if total_comments > 0 else 0, 1),
            
            # Project-style labels for modern dashboard
            'project_total': total_posts + total_pages,  # Total "projects" 
            'project_completed': published_posts,        # "Completed projects"
            'project_running': draft_posts,              # "Running projects"
            'project_pending': pending_comments,         # "Pending items"
        }
        
        if extra_context:
            context.update(extra_context)
            
        return super().index(request, context)


# Create custom admin site instance
custom_admin_site = CustomAdminSite(name='custom_admin')