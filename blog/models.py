from django.db import models
from user.models import BlogUser
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
class Banner(models.Model):
    title = models.CharField(max_length=20)
    position = models.IntegerField()
    img = models.ImageField(upload_to='banner/')
    url = models.CharField(max_length=512)
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

class Category(models.Model):
    name = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

class Tags(models.Model):
    name = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextUploadingField()
    user = models.ForeignKey(BlogUser)
    cover = models.ImageField(upload_to='article/')
    read_num = models.IntegerField(default=0)
    category = models.ForeignKey('Category',default=None)
    tags = models.ManyToManyField('Tags')
    pub_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    top = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name


class FriendLink(models.Model):
    name = models.CharField(max_length=20)
    url = models.CharField(max_length=512)
    position = models.IntegerField(default=0)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name

class Comment(models.Model):
    article = models.ForeignKey('Article')
    content = models.CharField(max_length=200)
    user = models.ForeignKey(BlogUser)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name