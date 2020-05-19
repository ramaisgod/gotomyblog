from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home_page'),
    path('blog/', home, name='home_page'),
    path('login/', login_page, name='login_page'),
    path('logout/', logout_page, name='logout_page'),
    path('change_password/', change_password, name='change_password'),
    path('signup/', signup, name='signup'),
    path('support/', support, name='support'),
    path('new_post/', new_post, name='new_post'),
    path('blog/saved_blog/', view_saved_blog, name='view_saved_blog'),
    path('blog/all_post/', all_post, name='all_post'),
    path('blog/search/', search, name='search'),
    path('blog/saved_blog/<int:post_id>/delete/', delete_saved_post, name='delete_saved_post'),
    path('blog/saved_blog/<int:post_id>/edit/', edit_saved_post, name='edit_saved_post'),
    path('blog/private_post/', view_private_post, name='view_private_post'),
    path('blog/private_post/<slug:slug>/', read_blog, name='read_blog'),
    path('blog/<str:blog_username>/', view_blog, name='view_blog'),
    path('blog/<str:blog_username>/<slug:slug>/', read_blog, name='read_blog'),
]
