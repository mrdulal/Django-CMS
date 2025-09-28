# Django CMS - Content Management System

A powerful and feature-rich Content Management System built with Django.

## Features

- **Rich Content Editor**: CKEditor integration with image upload support
- **User Management**: Authentication, authorization, and user profiles
- **Content Organization**: Categories and tags for better content organization
- **Comment System**: User comments with moderation capabilities
- **SEO Optimization**: Meta descriptions, SEO-friendly URLs, and structured content
- **Responsive Design**: Mobile-first Bootstrap design
- **Admin Dashboard**: Comprehensive dashboard for content management
- **Search Functionality**: Full-text search across posts
- **Media Management**: Image uploads and media library
- **Static Pages**: Create and manage static pages (About, Contact, etc.)

## Requirements

- Python 3.8+
- Django 4.2+
- SQLite (default) or PostgreSQL/MySQL
- Virtual environment (recommended)

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd /Users/sushridad/Python/CMS
   ```

2. **Virtual environment is already set up and activated**

3. **Required packages are already installed:**
   - Django
   - Pillow (for image handling)
   - django-ckeditor (rich text editor)
   - django-crispy-forms (form styling)
   - crispy-bootstrap4 (Bootstrap 4 styling)
   - django-taggit (tagging system)

4. **Database setup is complete:**
   - Migrations have been created and applied
   - Sample data has been loaded

## Usage

### Starting the Development Server

```bash
python manage.py runserver
```

The CMS will be available at `http://127.0.0.1:8000/`

### Admin Access

- **Admin URL**: `http://127.0.0.1:8000/admin/`
- **Username**: `admin`
- **Password**: `admin123`

### User Dashboard

- **Dashboard URL**: `http://127.0.0.1:8000/dashboard/`
- Available after logging in

## Project Structure

```
cms_project/
├── cms/                    # Main CMS app
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── forms.py           # Django forms
│   ├── admin.py           # Admin configuration
│   └── urls.py            # URL patterns
├── accounts/              # User authentication app
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── cms/              # CMS templates
│   └── accounts/         # Authentication templates
├── static/               # Static files (CSS, JS, Images)
├── media/                # User uploaded files
└── manage.py            # Django management script
```

## Models

### Post
- Title, slug, content, excerpt
- Author, category, tags
- Featured image, publication status
- SEO meta description
- Created/updated timestamps

### Category
- Name, slug, description
- Hierarchical organization

### Page
- Static pages (About, Contact, etc.)
- Similar to posts but without comments/categories

### Comment
- User comments on posts
- Moderation system (approved/pending)

### SiteSettings
- Global site configuration
- Social media links, branding
- Contact information

## Key Features Explained

### Content Creation
1. **Rich Text Editor**: Full-featured CKEditor with image upload
2. **Auto-slugs**: Automatic URL-friendly slug generation
3. **SEO Optimization**: Meta descriptions and structured data
4. **Category System**: Organize content with categories
5. **Tagging**: Flexible tagging system for content

### User Experience
1. **Responsive Design**: Works on all devices
2. **Search**: Full-text search across posts
3. **Comments**: User engagement through comments
4. **Navigation**: Category-based navigation
5. **Social Sharing**: Built-in social media sharing

### Administration
1. **Django Admin**: Full admin interface
2. **Custom Dashboard**: User-friendly dashboard
3. **Content Management**: Easy content creation/editing
4. **User Management**: User roles and permissions
5. **Comment Moderation**: Approve/reject comments

## Customization

### Themes
- Modify `static/css/style.css` for custom styling
- Bootstrap 5 framework for responsive design
- Easy color scheme customization

### Settings
- Modify `cms_project/settings.py` for configuration
- Database settings, media handling, etc.
- Email configuration for notifications

### Templates
- All templates in `templates/` directory
- Extend base template for consistent design
- Easy customization of layout and styling

## Sample Data

The CMS comes with sample data including:
- 5 blog posts across different categories
- 3 static pages (About, Contact, Privacy Policy)
- Site settings configuration
- Categories and tags

## Security Features

- CSRF protection on all forms
- SQL injection protection (Django ORM)
- XSS protection in templates
- User authentication and authorization
- Secure file upload handling

## Performance

- Database indexing on frequently queried fields
- Optimized queries with select_related and prefetch_related
- Static file serving optimization
- Image optimization support

## Deployment

For production deployment:

1. **Set DEBUG = False** in settings.py
2. **Configure production database** (PostgreSQL recommended)
3. **Set up static file serving** (whitenoise or nginx)
4. **Configure email backend** for notifications
5. **Set secure secret key**
6. **Enable HTTPS** and security headers

## API Endpoints

Main URLs:
- `/` - Homepage (post list)
- `/post/<slug>/` - Individual post
- `/page/<slug>/` - Static page
- `/category/<slug>/` - Category posts
- `/search/` - Search results
- `/dashboard/` - Admin dashboard
- `/accounts/login/` - Login page
- `/accounts/register/` - Registration
- `/admin/` - Django admin

## Contributing

1. Create feature branches
2. Write tests for new functionality
3. Follow Django coding standards
4. Update documentation
5. Submit pull requests

## License

This project is open source and available under the MIT License.

## Support

For questions or support:
- Check the Django documentation
- Review the code comments
- Create issues for bugs or feature requests

## Future Enhancements

Planned features:
- Newsletter subscription
- Advanced user roles
- Content scheduling
- Multi-language support
- REST API
- Theme system
- Plugin architecture