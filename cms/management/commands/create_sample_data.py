"""
Django management command to create sample data for the CMS
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cms.models import Category, Post, Page, SiteSettings
from django.utils import timezone
import random


class Command(BaseCommand):
    help = 'Create sample data for the CMS'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))
        
        # Create site settings
        site_settings, created = SiteSettings.objects.get_or_create(
            defaults={
                'site_title': 'My Django CMS',
                'site_description': 'A powerful content management system built with Django',
                'contact_email': 'contact@mycms.com',
                'footer_text': 'Built with Django CMS - A modern content management system',
            }
        )
        if created:
            self.stdout.write(f'Created site settings: {site_settings.site_title}')
        
        # Create categories
        categories_data = [
            {'name': 'Technology', 'description': 'Latest in technology and software development'},
            {'name': 'Web Development', 'description': 'Web development tutorials and tips'},
            {'name': 'Django', 'description': 'Django framework tutorials and guides'},
            {'name': 'Python', 'description': 'Python programming language content'},
            {'name': 'News', 'description': 'Latest news and updates'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Get or create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(f'Created admin user: {admin_user.username}')
        
        # Create sample posts
        posts_data = [
            {
                'title': 'Welcome to Our Django CMS',
                'content': '''
                    <h2>Welcome to our amazing Django CMS!</h2>
                    <p>This is a fully-featured content management system built with Django. It includes all the essential features you need to manage your website content effectively.</p>
                    
                    <h3>Features Include:</h3>
                    <ul>
                        <li>Rich text editor with image uploads</li>
                        <li>Category and tag management</li>
                        <li>User authentication and authorization</li>
                        <li>Comment system</li>
                        <li>SEO-friendly URLs</li>
                        <li>Responsive design</li>
                        <li>Admin dashboard</li>
                    </ul>
                    
                    <p>Start creating your content today!</p>
                ''',
                'excerpt': 'Welcome to our Django CMS! A powerful content management system with all the features you need.',
                'category': 'Django',
                'tags': ['django', 'cms', 'welcome'],
            },
            {
                'title': 'Getting Started with Django',
                'content': '''
                    <h2>Django: The Web Framework for Perfectionists</h2>
                    <p>Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of Web development, so you can focus on writing your app without needing to reinvent the wheel.</p>
                    
                    <h3>Why Choose Django?</h3>
                    <ul>
                        <li><strong>Fast:</strong> Django was designed to help developers take applications from concept to completion as quickly as possible.</li>
                        <li><strong>Secure:</strong> Django takes security seriously and helps developers avoid many common security mistakes.</li>
                        <li><strong>Scalable:</strong> Some of the busiest sites on the Web leverage Django's ability to quickly and flexibly scale.</li>
                    </ul>
                    
                    <p>Ready to get started? Check out our tutorials!</p>
                ''',
                'excerpt': 'Learn Django, the web framework for perfectionists with deadlines. Fast, secure, and scalable.',
                'category': 'Django',
                'tags': ['django', 'python', 'web-development'],
            },
            {
                'title': 'Modern Web Development Best Practices',
                'content': '''
                    <h2>Best Practices for Modern Web Development</h2>
                    <p>Web development has evolved significantly over the years. Here are some modern best practices that every developer should follow.</p>
                    
                    <h3>1. Responsive Design</h3>
                    <p>Ensure your website works well on all devices, from mobile phones to desktop computers.</p>
                    
                    <h3>2. Performance Optimization</h3>
                    <p>Optimize your code, images, and assets for fast loading times.</p>
                    
                    <h3>3. Accessibility</h3>
                    <p>Make your website accessible to users with disabilities.</p>
                    
                    <h3>4. SEO Optimization</h3>
                    <p>Structure your content and code to be search engine friendly.</p>
                    
                    <h3>5. Security</h3>
                    <p>Always follow security best practices to protect your users and data.</p>
                ''',
                'excerpt': 'Essential best practices for modern web development including responsive design, performance, and security.',
                'category': 'Web Development',
                'tags': ['web-development', 'best-practices', 'responsive'],
            },
            {
                'title': 'Python Tips and Tricks',
                'content': '''
                    <h2>Python Tips and Tricks for Better Code</h2>
                    <p>Python is known for its simplicity and readability, but there are always ways to write better, more efficient code.</p>
                    
                    <h3>List Comprehensions</h3>
                    <pre><code>squares = [x**2 for x in range(10)]</code></pre>
                    
                    <h3>Dictionary Comprehensions</h3>
                    <pre><code>word_lengths = {word: len(word) for word in words}</code></pre>
                    
                    <h3>The Zen of Python</h3>
                    <blockquote>
                        "Simple is better than complex.<br>
                        Complex is better than complicated.<br>
                        Readability counts."
                    </blockquote>
                    
                    <p>Remember: Write code that your future self will thank you for!</p>
                ''',
                'excerpt': 'Useful Python tips and tricks to write better, more efficient code.',
                'category': 'Python',
                'tags': ['python', 'tips', 'programming'],
            },
            {
                'title': 'The Future of Technology',
                'content': '''
                    <h2>Emerging Technologies Shaping Our Future</h2>
                    <p>Technology continues to evolve at a rapid pace. Here are some key trends that will shape the future.</p>
                    
                    <h3>Artificial Intelligence</h3>
                    <p>AI is transforming industries and changing how we interact with technology.</p>
                    
                    <h3>Internet of Things (IoT)</h3>
                    <p>Connected devices are creating smarter homes, cities, and workplaces.</p>
                    
                    <h3>Blockchain Technology</h3>
                    <p>Beyond cryptocurrency, blockchain is revolutionizing data security and transparency.</p>
                    
                    <h3>Edge Computing</h3>
                    <p>Processing data closer to where it's generated for faster, more efficient computing.</p>
                    
                    <p>Stay tuned for more insights on these exciting technologies!</p>
                ''',
                'excerpt': 'Explore emerging technologies like AI, IoT, and blockchain that are shaping our future.',
                'category': 'Technology',
                'tags': ['technology', 'ai', 'iot', 'blockchain'],
            }
        ]
        
        for post_data in posts_data:
            category = Category.objects.get(name=post_data['category'])
            post, created = Post.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    'content': post_data['content'],
                    'excerpt': post_data['excerpt'],
                    'author': admin_user,
                    'category': category,
                    'status': 'published',
                    'publish_date': timezone.now() - timezone.timedelta(days=random.randint(1, 30))
                }
            )
            
            if created:
                # Add tags
                for tag_name in post_data['tags']:
                    post.tags.add(tag_name)
                self.stdout.write(f'Created post: {post.title}')
        
        # Create sample pages
        pages_data = [
            {
                'title': 'About Us',
                'content': '''
                    <h2>About Our Django CMS</h2>
                    <p>Welcome to our content management system built with Django! We're passionate about creating powerful, user-friendly tools for managing web content.</p>
                    
                    <h3>Our Mission</h3>
                    <p>To provide a robust, scalable, and easy-to-use content management system that empowers users to create and manage their digital content effectively.</p>
                    
                    <h3>Features</h3>
                    <ul>
                        <li>Intuitive content editor</li>
                        <li>User management system</li>
                        <li>Category and tag organization</li>
                        <li>Comment moderation</li>
                        <li>SEO optimization tools</li>
                        <li>Responsive design</li>
                    </ul>
                    
                    <p>Thank you for choosing our CMS for your content management needs!</p>
                '''
            },
            {
                'title': 'Contact',
                'content': '''
                    <h2>Get in Touch</h2>
                    <p>We'd love to hear from you! Whether you have questions, feedback, or need support, don't hesitate to reach out.</p>
                    
                    <h3>Contact Information</h3>
                    <p><strong>Email:</strong> contact@mycms.com</p>
                    <p><strong>Support:</strong> support@mycms.com</p>
                    
                    <h3>Office Hours</h3>
                    <p>Monday - Friday: 9:00 AM - 6:00 PM (PST)</p>
                    <p>Saturday - Sunday: Closed</p>
                    
                    <p>We typically respond to inquiries within 24 hours during business days.</p>
                '''
            },
            {
                'title': 'Privacy Policy',
                'content': '''
                    <h2>Privacy Policy</h2>
                    <p><em>Last updated: [Date]</em></p>
                    
                    <h3>Information We Collect</h3>
                    <p>We collect information you provide directly to us, such as when you create an account, post content, or contact us.</p>
                    
                    <h3>How We Use Your Information</h3>
                    <p>We use the information we collect to provide, maintain, and improve our services.</p>
                    
                    <h3>Information Sharing</h3>
                    <p>We do not sell, trade, or otherwise transfer your personal information to third parties without your consent.</p>
                    
                    <h3>Data Security</h3>
                    <p>We implement appropriate security measures to protect your personal information.</p>
                    
                    <p>If you have any questions about this Privacy Policy, please contact us.</p>
                '''
            }
        ]
        
        for page_data in pages_data:
            page, created = Page.objects.get_or_create(
                title=page_data['title'],
                defaults={
                    'content': page_data['content'],
                    'is_published': True
                }
            )
            if created:
                self.stdout.write(f'Created page: {page.title}')
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write(self.style.SUCCESS('Admin credentials: username=admin, password=admin123'))