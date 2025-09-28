from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from .models import Category, Post, Page, Comment, SiteSettings
from .serializers import (
    UserSerializer, CategorySerializer, PostListSerializer, 
    PostDetailSerializer, PostCreateUpdateSerializer, PageSerializer, 
    CommentSerializer, SiteSettingsSerializer, DashboardStatsSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Category CRUD operations
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    lookup_field = 'slug'
    
    @action(detail=True, methods=['get'])
    def posts(self, request, slug=None):
        """Get all posts in this category"""
        category = self.get_object()
        posts = Post.objects.filter(
            category=category, 
            status='published'
        ).order_by('-publish_date')
        
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Post CRUD operations
    """
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'status', 'author']
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['created_at', 'updated_at', 'publish_date']
    ordering = ['-publish_date']
    lookup_field = 'slug'
    
    def get_queryset(self):
        """
        Return published posts for anonymous users,
        all posts for authenticated users
        """
        if self.request.user.is_authenticated:
            return Post.objects.all().select_related('author', 'category').prefetch_related('tags', 'comments')
        else:
            return Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags', 'comments')
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action
        """
        if self.action == 'list':
            return PostListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        else:
            return PostDetailSerializer
    
    def perform_create(self, serializer):
        """Set the author to the current user when creating a post"""
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_comment(self, request, slug=None):
        """Add a comment to this post"""
        post = self.get_object()
        
        data = request.data.copy()
        data['post'] = post.id
        
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def published(self, request):
        """Get only published posts"""
        posts = Post.objects.filter(status='published').order_by('-publish_date')
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = PostListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured posts (posts with featured images)"""
        posts = Post.objects.filter(
            status='published',
            featured_image__isnull=False
        ).exclude(featured_image='').order_by('-publish_date')[:10]
        
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)


class PageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Page CRUD operations
    """
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['title', 'created_at', 'updated_at']
    ordering = ['title']
    lookup_field = 'slug'
    
    def get_queryset(self):
        """
        Return published pages for anonymous users,
        all pages for authenticated users
        """
        if self.request.user.is_authenticated:
            return Page.objects.all()
        else:
            return Page.objects.filter(is_published=True)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Comment CRUD operations
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['post', 'is_approved']
    search_fields = ['name', 'email', 'content']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Return approved comments for anonymous users,
        all comments for authenticated users
        """
        if self.request.user.is_authenticated:
            return Comment.objects.all().select_related('post')
        else:
            return Comment.objects.filter(is_approved=True).select_related('post')
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def approve(self, request, pk=None):
        """Approve a comment"""
        comment = self.get_object()
        comment.is_approved = True
        comment.save()
        return Response({'status': 'comment approved'})
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reject(self, request, pk=None):
        """Reject a comment"""
        comment = self.get_object()
        comment.is_approved = False
        comment.save()
        return Response({'status': 'comment rejected'})


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for User read operations
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering_fields = ['username', 'date_joined']
    ordering = ['username']
    
    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        """Get all posts by this user"""
        user = self.get_object()
        posts = Post.objects.filter(author=user).order_by('-publish_date')
        
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)


class SiteSettingsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for SiteSettings
    """
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        # Return the first (and should be only) SiteSettings instance
        return SiteSettings.objects.all()[:1]


class DashboardViewSet(viewsets.ViewSet):
    """
    ViewSet for dashboard statistics and data
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        """Get dashboard statistics"""
        # Basic counts
        total_posts = Post.objects.count()
        published_posts = Post.objects.filter(status='published').count()
        draft_posts = Post.objects.filter(status='draft').count()
        total_comments = Comment.objects.count()
        pending_comments = Comment.objects.filter(is_approved=False).count()
        approved_comments = Comment.objects.filter(is_approved=True).count()
        total_categories = Category.objects.count()
        total_pages = Page.objects.count()
        total_users = User.objects.count()
        
        # Recent activity
        recent_posts = Post.objects.order_by('-created_at')[:5]
        recent_comments = Comment.objects.order_by('-created_at')[:5]
        
        # Popular categories
        popular_categories = Category.objects.annotate(
            post_count=Count('posts')
        ).order_by('-post_count')[:5]
        
        data = {
            'total_posts': total_posts,
            'published_posts': published_posts,
            'draft_posts': draft_posts,
            'total_comments': total_comments,
            'pending_comments': pending_comments,
            'approved_comments': approved_comments,
            'total_categories': total_categories,
            'total_pages': total_pages,
            'total_users': total_users,
            'recent_posts': recent_posts,
            'recent_comments': recent_comments,
            'popular_categories': popular_categories,
        }
        
        serializer = DashboardStatsSerializer(data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """Get analytics data for charts"""
        # Posts created over time (last 6 months)
        now = timezone.now()
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
            monthly_labels.append(month_date.strftime('%b %Y'))
        
        # Category distribution
        category_stats = Category.objects.annotate(
            post_count=Count('posts')
        ).values('name', 'post_count').order_by('-post_count')
        
        # Status distribution
        status_stats = Post.objects.values('status').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return Response({
            'monthly_posts': {
                'labels': monthly_labels,
                'data': monthly_data
            },
            'category_distribution': list(category_stats),
            'status_distribution': list(status_stats)
        })