from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Post, Page, Category, Comment, SiteSettings
from .forms import CommentForm, PostForm, PageForm


def get_site_settings():
    """Helper function to get site settings"""
    try:
        return SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        return None


class PostListView(ListView):
    model = Post
    template_name = 'cms/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = Post.objects.filter(status='published', publish_date__lte=timezone.now())
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(excerpt__icontains=search_query)
            )
        
        # Category filter
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Tag filter
        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__name=tag)
        
        return queryset.select_related('author', 'category').prefetch_related('tags')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['site_settings'] = get_site_settings()
        context['search_query'] = self.request.GET.get('search', '')
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'cms/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        return Post.objects.filter(status='published', publish_date__lte=timezone.now())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(is_approved=True)
        context['comment_form'] = CommentForm()
        context['site_settings'] = get_site_settings()
        context['related_posts'] = Post.objects.filter(
            status='published',
            category=self.object.category
        ).exclude(id=self.object.id)[:3]
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'cms/category_detail.html'
    context_object_name = 'category'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(
            category=self.object,
            status='published',
            publish_date__lte=timezone.now()
        ).select_related('author')
        
        paginator = Paginator(posts, 6)
        page_number = self.request.GET.get('page')
        context['posts'] = paginator.get_page(page_number)
        context['site_settings'] = get_site_settings()
        return context


class PageDetailView(DetailView):
    model = Page
    template_name = 'cms/page_detail.html'
    context_object_name = 'page'
    
    def get_queryset(self):
        return Page.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = get_site_settings()
        return context


@require_POST
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        messages.success(request, 'Your comment has been submitted and is awaiting approval.')
    else:
        messages.error(request, 'There was an error with your comment. Please try again.')
    
    return redirect('cms:post_detail', slug=slug)


@login_required
def dashboard(request):
    """Admin dashboard view"""
    context = {
        'total_posts': Post.objects.count(),
        'published_posts': Post.objects.filter(status='published').count(),
        'draft_posts': Post.objects.filter(status='draft').count(),
        'total_comments': Comment.objects.count(),
        'pending_comments': Comment.objects.filter(is_approved=False).count(),
        'total_categories': Category.objects.count(),
        'total_pages': Page.objects.count(),
        'recent_posts': Post.objects.order_by('-created_at')[:5],
        'recent_comments': Comment.objects.order_by('-created_at')[:5],
        'site_settings': get_site_settings(),
    }
    return render(request, 'cms/dashboard.html', context)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save many-to-many relationships (tags)
            messages.success(request, 'Post created successfully!')
            return redirect('cms:post_detail', slug=post.slug)
    else:
        form = PostForm()
    
    return render(request, 'cms/create_post.html', {'form': form})


@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('cms:post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'cms/edit_post.html', {'form': form, 'post': post})


@login_required
def create_page(request):
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save()
            messages.success(request, 'Page created successfully!')
            return redirect('cms:page_detail', slug=page.slug)
    else:
        form = PageForm()
    
    return render(request, 'cms/create_page.html', {'form': form})


def search_posts(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            status='published',
            publish_date__lte=timezone.now()
        ).select_related('author', 'category')
    else:
        posts = Post.objects.none()
    
    context = {
        'posts': posts,
        'query': query,
        'site_settings': get_site_settings(),
    }
    return render(request, 'cms/search_results.html', context)
