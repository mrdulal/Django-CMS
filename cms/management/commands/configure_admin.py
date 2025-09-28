"""
Django management command to configure admin interface theme
"""
from django.core.management.base import BaseCommand
from admin_interface.models import Theme


class Command(BaseCommand):
    help = 'Configure AdminLTE theme for admin interface'

    def handle(self, *args, **options):
        try:
            # Configure the admin interface theme
            theme, created = Theme.objects.get_or_create(
                name='CMS AdminLTE Theme',
                defaults={
                    'active': True,
                    'title': 'CMS Admin Dashboard',
                    'title_visible': True,
                    'logo': '',
                    'logo_visible': True,
                    'css_header_background_color': '#343a40',
                    'css_header_text_color': '#ffffff',
                    'css_header_link_color': '#ffffff',
                    'css_header_link_hover_color': '#c3c3c3',
                    'css_module_background_color': '#ffffff',
                    'css_module_text_color': '#333333',
                    'css_module_link_color': '#007bff',
                    'css_module_link_hover_color': '#0056b3',
                    'css_module_rounded_corners': True,
                    'css_generic_link_color': '#007bff',
                    'css_generic_link_hover_color': '#0056b3',
                    'css_save_button_background_color': '#28a745',
                    'css_save_button_background_hover_color': '#218838',
                    'css_save_button_text_color': '#ffffff',
                    'css_delete_button_background_color': '#dc3545',
                    'css_delete_button_background_hover_color': '#c82333',
                    'css_delete_button_text_color': '#ffffff',
                    'list_filter_dropdown': True,
                    'related_modal_active': True,
                    'related_modal_background_color': '#000000',
                    'related_modal_background_opacity': '0.3',
                    'env_name': '',
                    'env_visible_in_header': False,
                    'env_color': '#e74c3c',
                    'env_visible_in_favicon': False,
                    'language_chooser_active': False,
                    'language_chooser_display': 'code',
                    'list_filter_sticky': True,
                    'form_pagination_sticky': True,
                    'form_submit_sticky': True,
                    'css_module_background_selected_color': '#e8f4fd',
                    'css_module_link_selected_color': '#5b80b2'
                }
            )
            
            # Ensure the theme is active
            if not created:
                theme.active = True
                theme.save()
                self.stdout.write(
                    self.style.SUCCESS('Admin theme updated and activated successfully!')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS('Admin theme created and activated successfully!')
                )
                
            # Deactivate other themes
            Theme.objects.exclude(id=theme.id).update(active=False)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'AdminLTE theme configured: {theme.name}'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error configuring admin theme: {str(e)}')
            )