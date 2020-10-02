from django.db import models
from django.contrib.auth.models import User
# from home.models import Account as User
from django.utils.timezone import now

# Create your models here.

class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    views = models.IntegerField(default=0)
    slug = models.CharField(max_length=100)
    timeStamp = models.DateTimeField(default=now)

    def __str__(self):
        # return self.title + ' by ' + self.author
        return self.title + ' by ' + self.author.username


class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timeStamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] + "..." + " by " + self.user.username
    