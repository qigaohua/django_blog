# -*- coding: utf-8 -*-


from django import template
from ..models import Post, Category

register = template.Library()


@register.simple_tag
def get_recent_post(num=5):
    return Post.objects.all().order_by('-create_time')[:num]


@register.simple_tag
def archives():
    return Post.objects.dates('create_time', 'month', order='DESC')


@register.simple_tag
def get_category():
    category_list = Category.objects.all()
    return category_list



