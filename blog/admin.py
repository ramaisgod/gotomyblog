from django.contrib import admin
from .models import BlogPost, PostComment

admin.AdminSite.site_header = "GotoMyBlog - Admin Panel"
admin.AdminSite.site_title = "GotoMyBlog - Admin"
admin.AdminSite.index_title = "GotoMyBlog"

# Register your models here.
admin.site.register(PostComment)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/tinyinject.js', )


# class ArticleAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug": ("title",)}


