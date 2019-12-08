from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from PIL import  Image

# Create your models here.

class Column(models.Model):
    title = models.CharField('名称', max_length=100, blank=True)
    created_time = models.DateTimeField('创建时间',default=timezone.now)

    class Meta:
        verbose_name='栏目'
        verbose_name_plural='栏目'
        ordering = ('-created_time',)#按照降序排列，必须要有逗号，否则报错不是tupple

    def __str__(self):
        return self.title

class Post(models.Model):
    '''文章类，存储文章信息'''

    #标题
    title = models.CharField('标题',max_length=100)
    #标题图
    avatar = models.ImageField(upload_to='post/%Y%m%d', blank=True)
    #标签
    tags = TaggableManager(blank=True)
    #正文，内容比较多，使用text
    body = models.TextField('正文')
    likes = models.PositiveIntegerField(default=0)
    #创建时间和最后一次修改时间
    created_time = models.DateTimeField('创建时间',default=timezone.now)
    modified_time = models.DateTimeField('修改时间',auto_now=True)#指定修改后自动更新时间
    #作者，使用Django自带的User管理类
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    total_views = models.PositiveIntegerField('浏览',default=0)
    column = models.ForeignKey(Column, verbose_name='栏目', null=True, blank=True,
                               on_delete=models.CASCADE,related_name='post')
    def save(self, *args, **kwargs):
        post = super(Post, self).save(*args, **kwargs)
        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x,y) = image.size
            new_x = 400
            new_y = int(new_x * (y/x))
            resized_image = image.resize((new_x,new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)
        return post

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])#路由重定向


    class Meta:
        verbose_name='文章'
        verbose_name_plural='文章'
        ordering = ('-created_time',)#按照降序排列，必须要有逗号，否则报错不是tupple

    def __str__(self):
        return self.title

