from django.db import models
from user.models import UserProfile

# Create your models here.

class Topic(models.Model):
    title = models.CharField(max_length=50,verbose_name='文章主题')
    # tec 技术类文章  no-tec 非技术类文章
    category = models.CharField(max_length=20,verbose_name='文章分类')
    # public 公开博客  private 私有博客
    limit = models.CharField(max_length=10,verbose_name='文章权限')
    introduce = models.CharField(max_length=90,verbose_name='文章简介')
    content = models.TextField(verbose_name='文章内容')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')
    author = models.ForeignKey(UserProfile)

    class Meta:
        db_table = 'topic'