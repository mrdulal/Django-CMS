from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Category, Post, Page, Comment, SiteSettings
from .admin_site import custom_admin_site


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    ordering = ['name']
    readonly_fields = ['created_at']
    
    def post_count(self, obj):
        count = obj.posts.count()
        url = reverse('admin:cms_post_changelist') + f'?category__id__exact={obj.id}'
        return format_html('<a href="{}">{} posts</a>', url, count)
    
    post_count.short_description = 'Posts'
    post_count.admin_order_field = 'posts__count'
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('posts')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'comment_count', 'publish_date', 'created_at']
    list_filter = ['status', 'category', 'created_at', 'publish_date', 'author']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_date'
    ordering = ['-publish_date']
    raw_id_fields = ['author']
    list_editable = ['status']
    list_per_page = 20
    actions = ['make_published', 'make_draft']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'category', 'status'),
            'classes': ('wide',)
        }),
        ('Content', {
            'fields': ('content', 'excerpt', 'featured_image'),
            'classes': ('wide',)
        }),
        ('SEO & Meta', {
            'fields': ('meta_description', 'tags'),
            'classes': ('collapse', 'wide'),
            'description': 'Search Engine Optimization settings'
        }),
        ('Publishing', {
            'fields': ('publish_date',),
            'classes': ('wide',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def status_badge(self, obj):
        if obj.status == 'published':
            return format_html('<span class="badge badge-success">Published</span>')
        else:
            return format_html('<span class="badge badge-warning">Draft</span>')
    
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'
    
    def comment_count(self, obj):
        count = obj.comments.count()
        approved_count = obj.comments.filter(is_approved=True).count()
        url = reverse('admin:cms_comment_changelist') + f'?post__id__exact={obj.id}'
        return format_html('<a href="{}">{} comments ({} approved)</a>', url, count, approved_count)
    
    comment_count.short_description = 'Comments'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new post
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    def make_published(self, request, queryset):
        queryset.update(status='published')
        self.message_user(request, f'{queryset.count()} posts were successfully published.')
    make_published.short_description = "Mark selected posts as published"
    
    def make_draft(self, request, queryset):
        queryset.update(status='draft')
        self.message_user(request, f'{queryset.count()} posts were moved to draft.')
    make_draft.short_description = "Mark selected posts as draft"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'category').prefetch_related('comments')


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_published', 'created_at', 'updated_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'is_published'),
            'classes': ('wide',)
        }),
        ('Content', {
            'fields': ('content',),
            'classes': ('wide',)
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse', 'wide')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_published_badge(self, obj):
        if obj.is_published:
            return format_html('<span class="badge badge-success">Published</span>')
        else:
            return format_html('<span class="badge badge-secondary">Draft</span>')
    
    is_published_badge.short_description = 'Status'
    is_published_badge.admin_order_field = 'is_published'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post_link', 'is_approved', 'created_at', 'email']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['name', 'email', 'content', 'post__title']
    ordering = ['-created_at']
    list_editable = ['is_approved']
    actions = ['approve_comments', 'reject_comments']
    list_per_page = 20
    
    fieldsets = (
        ('Comment Information', {
            'fields': ('name', 'email', 'post', 'is_approved'),
            'classes': ('wide',)
        }),
        ('Content', {
            'fields': ('content',),
            'classes': ('wide',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at']
    
    def post_link(self, obj):
        url = reverse('admin:cms_post_change', args=[obj.post.id])
        return format_html('<a href="{}">{}</a>', url, obj.post.title[:50])
    
    post_link.short_description = 'Post'
    post_link.admin_order_field = 'post__title'
    
    def is_approved_badge(self, obj):
        if obj.is_approved:
            return format_html('<span class="badge badge-success">Approved</span>')
        else:
            return format_html('<span class="badge badge-warning">Pending</span>')
    
    is_approved_badge.short_description = 'Status'
    is_approved_badge.admin_order_field = 'is_approved'
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} comments were approved.')
    approve_comments.short_description = "Approve selected comments"
    
    def reject_comments(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f'{queryset.count()} comments were rejected.')
    reject_comments.short_description = "Reject selected comments"
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('post')


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_title', 'site_description', 'contact_email'),
            'classes': ('wide',)
        }),
        ('Social Media', {
            'fields': ('social_facebook', 'social_twitter', 'social_instagram', 'social_linkedin'),
            'classes': ('collapse', 'wide'),
            'description': 'Social media profile URLs'
        }),
        ('Branding', {
            'fields': ('logo', 'favicon', 'footer_text'),
            'classes': ('collapse', 'wide'),
            'description': 'Site branding and visual elements'
        }),
    )
    
    def has_add_permission(self, request):
        # Allow only one instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False


# Register models with custom admin site as well
custom_admin_site.register(Category, CategoryAdmin)
custom_admin_site.register(Post, PostAdmin)
custom_admin_site.register(Page, PageAdmin)
custom_admin_site.register(Comment, CommentAdmin)
custom_admin_site.register(SiteSettings, SiteSettingsAdmin)
