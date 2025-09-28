from django.contrib.admin import AdminSite
from django.contrib.auth.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Post, Comment, Page, Category
from django.contrib.auth.models import User


@staff_member_required
def admin_dashboard(request):
    """
    Custom admin dashboard view with enhanced analytics
    """
    # Get current date
    now = timezone.now()
    
    # Basic statistics
    total_posts = Post.objects.count()
    published_posts = Post.objects.filter(status='published').count()
    draft_posts = Post.objects.filter(status='draft').count()
    total_pages = Page.objects.count()
    pending_comments = Comment.objects.filter(is_approved=False).count()
    total_comments = Comment.objects.count()
    approved_comments = Comment.objects.filter(is_approved=True).count()
    
    # Recent posts (last 10)
    recent_posts = Post.objects.select_related('author', 'category').order_by('-created_at')[:10]
    
    # Recent comments (last 10)
    recent_comments = Comment.objects.select_related('post').order_by('-created_at')[:10]
    
    # Monthly data for charts (last 6 months)
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
    
    # User activity
    total_users = User.objects.count()
    active_users = User.objects.filter(last_login__gte=now - timedelta(days=30)).count()
    
    # Category statistics
    categories_with_counts = Category.objects.annotate(
        post_count=Count('posts')
    ).order_by('-post_count')[:5]
    
    # Top authors
    top_authors = User.objects.annotate(
        post_count=Count('posts')
    ).filter(post_count__gt=0).order_by('-post_count')[:5]
    
    # Comments by status
    approved_comments_percentage = (approved_comments / total_comments * 100) if total_comments > 0 else 0
    pending_comments_percentage = (pending_comments / total_comments * 100) if total_comments > 0 else 0
    
    # Weekly activity (last 7 days)
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
    
    context = {
        'title': 'Dashboard',
        'subtitle': 'Plan, projects and accomplish your tasks with ease.',
        
        # Main statistics
        'total_posts': total_posts,
        'published_posts': published_posts,
        'draft_posts': draft_posts,
        'total_pages': total_pages,
        'pending_comments': pending_comments,
        'total_comments': total_comments,
        'approved_comments': approved_comments,
        'total_users': total_users,
        'active_users': active_users,
        
        # Chart data
        'monthly_data': monthly_data,
        'monthly_labels': monthly_labels,
        'weekly_data': weekly_data,
        'weekly_labels': weekly_labels,
        
        # Recent activity
        'recent_posts': recent_posts,
        'recent_comments': recent_comments,
        
        # Analytics
        'categories_with_counts': categories_with_counts,
        'top_authors': top_authors,
        'approved_comments_percentage': round(approved_comments_percentage, 1),
        'pending_comments_percentage': round(pending_comments_percentage, 1),
        
        # Additional metrics
        'posts_this_month': Post.objects.filter(
            created_at__gte=now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        ).count(),
        'comments_this_month': Comment.objects.filter(
            created_at__gte=now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        ).count(),
        
        # Performance indicators
        'avg_posts_per_day': round(total_posts / max((now - recent_posts.last().created_at).days, 1) if recent_posts.exists() else 0, 1),
        'engagement_rate': round((total_comments / total_posts * 100) if total_posts > 0 else 0, 1),
    }
    
    return render(request, 'admin/index.html', context)


def get_dashboard_stats():
    """
    Helper function to get dashboard statistics
    """
    now = timezone.now()
    
    return {
        'total_posts': Post.objects.count(),
        'published_posts': Post.objects.filter(status='published').count(),
        'draft_posts': Post.objects.filter(status='draft').count(),
        'pending_comments': Comment.objects.filter(is_approved=False).count(),
        'total_pages': Page.objects.count(),
        'recent_posts': Post.objects.select_related('author', 'category').order_by('-created_at')[:5],
        'recent_comments': Comment.objects.select_related('post').order_by('-created_at')[:5],
    }