from django.core.management.base import BaseCommand
from admin_interface.models import Theme


class Command(BaseCommand):
    help = 'Configure admin interface theme'

    def handle(self, *args, **options):
        theme, created = Theme.objects.get_or_create(
            name='Django CMS',
            defaults={
                'active': True,
                'title': 'Django CMS Admin',
                'title_visible': True,
                'css_header_background_color': '#667eea',
                'css_header_text_color': '#ffffff',
                'css_header_link_color': '#ffffff',
                'css_header_link_hover_color': '#f8f9fa',
                'css_module_background_color': '#ffffff',
                'css_module_text_color': '#333333',
                'css_module_link_color': '#667eea',
                'css_module_link_hover_color': '#5a67d8',
                'css_generic_link_color': '#667eea',
                'css_generic_link_hover_color': '#5a67d8',
                'css_save_button_background_color': '#667eea',
                'css_save_button_background_hover_color': '#5a67d8',
                'css_save_button_text_color': '#ffffff',
                'list_filter_dropdown': True,
                'related_modal_active': True,
                'related_modal_background_color': '#000000',
                'related_modal_background_opacity': 0.3,
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created theme: {theme.name}')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Theme already exists: {theme.name}')
            )