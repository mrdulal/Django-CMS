from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Post, Page, Comment, SiteSettings


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    post_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at', 'post_count']
        read_only_fields = ['id', 'created_at', 'post_count']
    
    def get_post_count(self, obj):
        return obj.posts.filter(status='published').count()


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model"""
    post_title = serializers.CharField(source='post.title', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'post_title', 'name', 'email', 'content', 'is_approved', 'created_at']
        read_only_fields = ['id', 'created_at', 'post_title']


class PostListSerializer(serializers.ModelSerializer):
    """Serializer for Post list view (lighter version)"""
    author = serializers.CharField(source='author.get_full_name', read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    comment_count = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'excerpt', 'author', 'author_username', 
            'category', 'category_name', 'status', 'featured_image', 
            'publish_date', 'created_at', 'updated_at', 'comment_count', 'tags'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'comment_count', 'tags']
    
    def get_comment_count(self, obj):
        return obj.comments.filter(is_approved=True).count()
    
    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]


class PostDetailSerializer(serializers.ModelSerializer):
    """Serializer for Post detail view (full version)"""
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    tags = serializers.SerializerMethodField()
    approved_comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt', 'author', 'category', 
            'status', 'featured_image', 'meta_description', 'publish_date', 
            'created_at', 'updated_at', 'tags', 'comments', 'approved_comments'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'comments', 'approved_comments']
    
    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]
    
    def get_approved_comments(self, obj):
        approved_comments = obj.comments.filter(is_approved=True).order_by('-created_at')
        return CommentSerializer(approved_comments, many=True).data


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating posts"""
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False,
        allow_empty=True
    )
    
    class Meta:
        model = Post
        fields = [
            'title', 'content', 'excerpt', 'category', 'status', 
            'featured_image', 'meta_description', 'publish_date', 'tags'
        ]
    
    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        post = Post.objects.create(**validated_data)
        
        # Add tags
        for tag_name in tags_data:
            post.tags.add(tag_name)
        
        return post
    
    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        
        # Update post fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update tags if provided
        if tags_data is not None:
            instance.tags.clear()
            for tag_name in tags_data:
                instance.tags.add(tag_name)
        
        return instance


class PageSerializer(serializers.ModelSerializer):
    """Serializer for Page model"""
    class Meta:
        model = Page
        fields = ['id', 'title', 'slug', 'content', 'meta_description', 'is_published', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class SiteSettingsSerializer(serializers.ModelSerializer):
    """Serializer for SiteSettings model"""
    class Meta:
        model = SiteSettings
        fields = [
            'site_title', 'site_description', 'contact_email', 'logo', 'favicon',
            'footer_text', 'social_facebook', 'social_twitter', 'social_instagram', 
            'social_linkedin'
        ]


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics"""
    total_posts = serializers.IntegerField()
    published_posts = serializers.IntegerField()
    draft_posts = serializers.IntegerField()
    total_comments = serializers.IntegerField()
    pending_comments = serializers.IntegerField()
    approved_comments = serializers.IntegerField()
    total_categories = serializers.IntegerField()
    total_pages = serializers.IntegerField()
    total_users = serializers.IntegerField()
    recent_posts = PostListSerializer(many=True)
    recent_comments = CommentSerializer(many=True)
    popular_categories = CategorySerializer(many=True)