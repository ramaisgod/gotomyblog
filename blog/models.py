from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid


# Create your models here.
class BlogPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=20)
    timestamp = models.DateTimeField(default=now)
    # slug = models.SlugField(unique=True, default=uuid.uuid1)
    slug = models.CharField(max_length=255, unique=True, default=uuid.uuid1, editable=False)
    private = models.BooleanField(default=False)
    published = models.BooleanField(default=True)
    blog_username = models.CharField(max_length=20)

    def __str__(self):
        return self.title[:20] + "... [ post by " + self.user.username + " ]"

    def save(self, *args, **kwargs):
        if not self.post_id:
            timestamp = now().strftime("%y%m%d-%H%M%S-%f")
            self.slug = slugify(str(self.title)[0:200] + "-" + str(timestamp) + uuid.uuid1().hex[:5])
            super(BlogPost, self).save(*args, **kwargs)
        else:
            super(BlogPost, self).save(*args, **kwargs)


class PostComment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[:10] + "... [ by " + self.user.username + " ]"
