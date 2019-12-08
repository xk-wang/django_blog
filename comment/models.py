from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
from django.contrib.auth.models import User
from blog.models import Post
from ckeditor.fields import RichTextField
import re

# Create your models here.
class Comment(MPTTModel):
    post = models.ForeignKey(Post,verbose_name='文章',on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User,verbose_name='用户',on_delete=models.CASCADE, related_name='comments')
    body = RichTextField(verbose_name='主体')
    created_time = models.DateTimeField(auto_now=True)

    parent = TreeForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='children')
    reply_to = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='replyers')


    class MPTTMeta:
        order_insertion_by = ['-created_time']

        # ordering=('-created_time', )
    # class Meta:
    #     verbose_name = '评论'
    #     verbose_name_plural = '评论'
    #     ordering = ('-created_time',)

    def __str__(self):
        return (re.sub(r'</?\w+[^>]*>','',self.body)).split('\n')[0]