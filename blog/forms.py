from django import forms
from .models import BlogPost, PostComment


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = '__all__'
