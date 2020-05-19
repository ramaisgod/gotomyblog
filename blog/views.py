from django.shortcuts import render, redirect, reverse, HttpResponseRedirect, HttpResponse
from .models import BlogPost, PostComment
from django.contrib import messages
from .forms import BlogForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now


# Create your views here.
def home(request):
    return render(request, 'blog/index.html', {})


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        path = request.META['HTTP_REFERER']
        if user:
            login(request, user)
            messages.success(request, "Login Success !!!")
            try:
                return HttpResponseRedirect(path)
            except:
                return HttpResponseRedirect(reverse(home))
        else:
            messages.warning(request, "Invalid Credential !!!")
            try:
                return HttpResponseRedirect(path)
            except:
                return HttpResponseRedirect(reverse(home))
    return render(request, 'blog/index.html', {})


def logout_page(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Logout Successfully !!!")
        return HttpResponseRedirect(reverse(home))


def change_password(request):
    if request.method == 'POST':
        new_pass1 = request.POST['newPassword1']
        new_pass2 = request.POST['newPassword2']
        if len(new_pass1) < 8:
            msg = "Password length should be minimum 8  !!!"
            messages.warning(request, msg)
            return HttpResponseRedirect(reverse(home))
        if new_pass1 != new_pass2:
            msg = "Confirm Password does not match !!!"
            messages.warning(request, msg)
            return HttpResponseRedirect(reverse(home))
        obj_User = User.objects.get(id=request.user.id)
        obj_User.set_password(new_pass1)
        obj_User.save()
        messages.success(request, "Password has been changed successfully !!!")
        return HttpResponseRedirect(reverse(home))


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        # Check if username already exist
        usernameCount = User.objects.filter(username=username).count()
        emailCount = User.objects.filter(email=email).count()
        if len(username) > 20:
            msg = "Username must be below 20 characters !!!"
            messages.warning(request, msg)
            return HttpResponseRedirect(reverse(home))
        if not username.isalnum():
            msg = "Username should be letters and numbers only !!!"
            messages.warning(request, msg)
            return HttpResponseRedirect(reverse(home))
        if usernameCount > 0:
            msg = "Username already exists !!!"
            messages.warning(request, msg)
            return HttpResponseRedirect(reverse(home))
        if emailCount > 0:
            msg = "Email already exists !!!"
            messages.warning(request, msg)
            return HttpResponseRedirect(reverse(home))
        if len(password) < 8:
            msg = "Password length should be minimum 8  !!!"
            messages.warning(request, msg)
            return HttpResponseRedirect(reverse(home))
        if password != confirm_password:
            msg = "Confirm Password does not match !!!"
            messages.warning(request, msg)
            return HttpResponseRedirect(reverse(home))
        if password != confirm_password:
            msg = "Confirm Password does not match !!!"
            messages.warning(request, msg)
            return HttpResponseRedirect(reverse(home))

        obj_User = User.objects.create_user(username=username, email=email, password=password)
        obj_User.first_name = f_name
        obj_User.last_name = l_name
        obj_User.save()
        messages.success(request, "GotoMyBlog account has been created successfully !!!")
        return HttpResponseRedirect(reverse(home))
    return render(request, 'blog/index.html', {})


@login_required(login_url='/')
def new_post(request):
    if (request.method == 'POST') and ('publish' in request.POST):
        postTitle = request.POST['postTitle']
        postAuthor = request.POST['postAuthor']
        postContent = request.POST['postContent']
        privatePost = request.POST.get('privatePost')
        user = request.user
        obj = BlogPost(user=user, title=postTitle, content=postContent, author=postAuthor, published=True, blog_username=request.user.username)
        if privatePost == "on":
            private = True
        else:
            private = False

        obj.private = private
        obj.save()
        messages.success(request, "Post has been published successfully !!!")
        return render(request, 'blog/new_post.html', {})
    elif (request.method == 'POST') and ('save_as_draft' in request.POST):
        postTitle = request.POST['postTitle']
        postAuthor = request.POST['postAuthor']
        postContent = request.POST['postContent']
        privatePost = request.POST.get('privatePost')
        print(privatePost)
        user = request.user
        obj = BlogPost(user=user, title=postTitle, content=postContent, author=postAuthor, published=False, blog_username=request.user.username)
        if privatePost == "on":
            private = True
        else:
            private = False

        obj.private = private
        obj.save()
        messages.success(request, "Post has been saved in draft !!!")
        return render(request, 'blog/new_post.html', {})
    return render(request, 'blog/new_post.html', {})


@login_required(login_url='/')
def edit_saved_post(request, post_id):
    blog_username = request.user.username
    obj_Blog = BlogPost.objects.get(user=request.user.id, post_id=post_id)
    form = BlogForm(instance=obj_Blog)
    if (request.method == 'POST') and ('publish' in request.POST):
        privatePost = request.POST.get('private')
        postTitle = request.POST['title']
        postAuthor = request.POST['author']
        postContent = request.POST['content']
        obj_Blog.title = postTitle
        obj_Blog.author = postAuthor
        obj_Blog.content = postContent
        if privatePost == "on":
            private = True
        else:
            private = False
        obj_Blog.private = private
        obj_Blog.published = True
        obj_Blog.timestamp = now()
        obj_Blog.save()
        messages.success(request, "Post has been published successfully !!!")
        return HttpResponseRedirect(reverse(view_saved_blog))
    elif (request.method == 'POST') and ('save_as_draft' in request.POST):
        privatePost = request.POST.get('private')
        postTitle = request.POST['title']
        postAuthor = request.POST['author']
        postContent = request.POST['content']
        obj_Blog.title = postTitle
        obj_Blog.author = postAuthor
        obj_Blog.content = postContent
        if privatePost == "on":
            private = True
        else:
            private = False
        obj_Blog.private = private
        obj_Blog.published = False
        obj_Blog.timestamp = now()
        obj_Blog.save()
        messages.success(request, "Post has been saved in draft !!!")
        return HttpResponseRedirect(reverse(view_saved_blog))
    return render(request, 'blog/edit_post.html', {'form': form, 'obj_Blog': obj_Blog})


@login_required(login_url='/')
def delete_saved_post(request, post_id):
    obj_Blog = BlogPost.objects.get(user=request.user.id, post_id=post_id)
    if request.method == 'POST':
        obj_Blog.delete()
        messages.success(request, "Post has been deleted successfully !!!")
        path = request.META['HTTP_REFERER']
        # return HttpResponseRedirect(reverse(view_saved_blog))
        return HttpResponseRedirect(path)


@login_required(login_url='/')
def post_comment(request, blog_username, slug=None):
    if request.method == 'POST':
        postComment = request.POST.get('postComment')
        postID = request.POST.get('postID')
        post = BlogPost.objects.get(post_id=postID)
        user = request.user
        parentID = request.POST.get('parentID')
        # postReply = request.POST['postReply']
        if parentID == "":
            comment = PostComment(comment=postComment, user=user, post=post)
            comment.save()
            messages.success(request, "Comments has been posted !!!")
        else:
            parent = PostComment.objects.get(comment_id=parentID)
            comment = PostComment(comment=postComment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "Reply has been posted !!!")
    return redirect(f"/blog/{blog_username}/{post.slug}/")


@login_required(login_url='/')
def view_saved_blog(request):
    obj_Blog = BlogPost.objects.filter(user=request.user.id, published=False).order_by('-timestamp')
    return render(request, 'blog/saved_blog.html', {'obj_Blog': obj_Blog})


def view_blog(request, blog_username):
    obj_Blog = BlogPost.objects.filter(blog_username=blog_username, published=True, private=False).order_by('-timestamp')
    return render(request, 'blog/view_blog.html', {'obj_Blog': obj_Blog})


def all_post(request):
    obj_Blog = BlogPost.objects.filter(user=request.user.id)
    return render(request, 'blog/all_post.html', {'obj_Blog': obj_Blog})


@login_required(login_url='/')
def view_private_post(request):
    obj_Blog = BlogPost.objects.filter(user=request.user.id, published=True, private=True).order_by('-timestamp')
    return render(request, 'blog/view_blog.html', {'obj_Blog': obj_Blog, 'private_blog': True})


def read_blog(request, slug, blog_username=None):
    post = BlogPost.objects.get(slug=slug)
    comments = PostComment.objects.filter(post=post, parent=None).order_by('-timestamp')
    replies = PostComment.objects.filter(post=post).exclude(parent=None).order_by('timestamp')
    context = {
        'post': post,
        'comments': comments,
        'replies': replies
    }
    if request.method == 'POST':
        postComment = request.POST.get('postComment')
        postID = request.POST.get('postID')
        post = BlogPost.objects.get(post_id=postID)
        user = request.user
        parentID = request.POST.get('parentID')
        # postReply = request.POST['postReply']
        if parentID == "":
            comment = PostComment(comment=postComment, user=user, post=post)
            comment.save()
            messages.success(request, "Comments has been posted !!!")
        else:
            parent = PostComment.objects.get(comment_id=parentID)
            comment = PostComment(comment=postComment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "Reply has been posted !!!")
    return render(request, 'blog/read_blog.html', context)


def search(request, blog_username=None):
    searchText = request.GET['searchText'].strip()
    if len(searchText) < 1:
        obj_Blog = BlogPost.objects.none()
        return render(request, 'blog/search_blog.html', {'obj_Blog': obj_Blog, 'searchText': searchText})
    if len(searchText) > 32:
        obj_Blog = BlogPost.objects.none()
        return render(request, 'blog/search_blog.html', {'obj_Blog': obj_Blog, 'searchText': searchText})
    else:
        obj_BlogTitle = BlogPost.objects.filter(title__icontains=searchText, published=True, private=False)
        obj_BlogContent = BlogPost.objects.filter(content__icontains=searchText, published=True, private=False)
        obj_Blog = obj_BlogTitle.union(obj_BlogContent)
        return render(request, 'blog/search_blog.html', {'obj_Blog': obj_Blog, 'searchText': searchText})


def support(request):
    return render(request, 'blog/support.html', {})
