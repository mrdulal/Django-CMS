from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, Submit, HTML
from crispy_forms.bootstrap import AppendedText, PrependedText
from .models import Comment, Post, Page, Category


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(Field('name'), css_class='col-md-6'),
                Div(Field('email'), css_class='col-md-6'),
                css_class='row'
            ),
            Field('content'),
            Submit('submit', 'Post Comment', css_class='btn btn-primary')
        )


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title', 'slug', 'category', 'content', 'excerpt', 
            'featured_image', 'status', 'publish_date', 'meta_description', 'tags'
        ]
        widgets = {
            'publish_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'excerpt': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Basic Information',
                Div(
                    Div(Field('title'), css_class='col-md-8'),
                    Div(Field('slug'), css_class='col-md-4'),
                    css_class='row'
                ),
                Div(
                    Div(Field('category'), css_class='col-md-6'),
                    Div(Field('status'), css_class='col-md-6'),
                    css_class='row'
                ),
            ),
            Fieldset(
                'Content',
                Field('content'),
                Field('excerpt'),
                Field('featured_image'),
            ),
            Fieldset(
                'SEO & Publishing',
                Field('meta_description'),
                Field('tags'),
                Field('publish_date'),
                css_class='collapse show'
            ),
            Submit('submit', 'Save Post', css_class='btn btn-primary')
        )


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'slug', 'content', 'meta_description', 'is_published']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(Field('title'), css_class='col-md-8'),
                Div(Field('slug'), css_class='col-md-4'),
                css_class='row'
            ),
            Field('content'),
            Field('meta_description'),
            Field('is_published'),
            Submit('submit', 'Save Page', css_class='btn btn-primary')
        )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(Field('name'), css_class='col-md-6'),
                Div(Field('slug'), css_class='col-md-6'),
                css_class='row'
            ),
            Field('description'),
            Submit('submit', 'Save Category', css_class='btn btn-primary')
        )