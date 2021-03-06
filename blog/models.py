# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.html import strip_tags
import markdown

# Create your models here.


# 分类
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# 标签
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# 文章
class Post(models.Model):
    # 标题
    title = models.CharField(max_length=100, verbose_name='标题')

    # 正文
    body = models.TextField(verbose_name='正文')

    # 创建时间和最后修改时间
    create_time = models.DateTimeField(verbose_name='创建时间')
    modified_time = models.DateTimeField(verbose_name='修改时间')

    # 摘要
    excerpt = models.CharField(max_length=200, blank=True, verbose_name='摘要')
    views = models.PositiveIntegerField(default=0)

    # 分类与标签
    category = models.ForeignKey(Category, verbose_name='分类')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')

    auther = models.ForeignKey(User, verbose_name='作者')

    def __str__(self):
        return self.title

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                                            'markdown.extensions.extra',
                                            'markdown.extensions.codehilite',
                                            'markdown.extensions.toc',
                                                        ])
            self.excerpt = strip_tags(md.convert(self.body))[:100]

        super(Post, self).save(*args, **kwargs)

