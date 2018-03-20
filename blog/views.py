# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from django import template
from .models import Post, Category
from comments.forms import CommentForm
import markdown


# Create your views here.
def hello(request):
    # return HttpResponse("欢迎访问我的博客")
    # text = template.Context({'title': '我的博客首页', 'welcome': '欢迎访问我的博客！！！'})
    return render(request, 'blog/hello.html', context={
                             'title': '我的博客首页', 
                             'welcome': '欢迎访问我的博客！！！'})


def index(request):
    list = Post.objects.all().order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list': list})


def archives(request, year, month):
    list = Post.objects.filter(create_time__year=year,
                               create_time__month=month).order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list': list})


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    list = Post.objects.filter(category=cate).order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list': list})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body, extensions=[
                                            'markdown.extensions.extra',
                                            'markdown.extensions.codehilite',
                                            'markdown.extensions.toc',
                                                        ])

    post.increase_views()
    form = CommentForm()
    comment_list = post.comment_set.all()

    context = {'post': post, 'form': form, 'comment_list': comment_list}
    return render(request, 'blog/detail.html', context=context)


