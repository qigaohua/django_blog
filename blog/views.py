# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from django import template
from .models import Post, Category
from comments.forms import CommentForm
import markdown
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def hello(request):
    # return HttpResponse("欢迎访问我的博客")
    # text = template.Context({'title': '我的博客首页', 'welcome': '欢迎访问我的博客！！！'})
    return render(request, 'blog/hello.html', context={
                             'title': '我的博客首页', 
                             'welcome': '欢迎访问我的博客！！！'})


def index(request):
    #page_obj = {}
    list = Post.objects.all().order_by('-create_time')
    paginator = Paginator(list, 6)

    if list.count > 3:
        is_page = True
    else:
        is_page = False

    page = request.GET.get('page')
    try:
        list_page = paginator.page(page)
    except PageNotAnInteger:
        list_page = paginator.page(1)
    except EmptyPage:
        list_page = paginator.page(paginator.num_pages)
    '''
    if list_page.has_previous:
        page_obj['previous'] = True
    else:
        page_obj['previous'] = False

    if list_page.has_next:
        page_obj['next'] = True
    else:
        page_obj['next'] = False

    page_obj['previous_page_number'] = list_page.previous_page_number
    print list_page.has_previous
    print list_page.has_next
    '''
    return render(request, 'blog/index.html', context={'post_list': list_page, 
                                                       "is_paginated": is_page})


def archives(request, year, month):
    list = Post.objects.filter(create_time__year=year,
                               create_time__month=month).order_by('-create_time')
    paginator = Paginator(list, 6)

    if list.count > 3:
        is_page = True
    else:
        is_page = False

    page = request.GET.get('page')
    try:
        list_page = paginator.page(page)
    except PageNotAnInteger:
        list_page = paginator.page(1)
    except EmptyPage:
        list_page = paginator.page(paginator.num_pages)

    return render(request, 'blog/index.html', context={'post_list': list_page,
                                                    "is_paginated": is_page})



def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    list = Post.objects.filter(category=cate).order_by('-create_time')

    paginator = Paginator(list, 6)

    if list.count > 3:
        is_page = True
    else:
        is_page = False

    page = request.GET.get('page')
    try:
        list_page = paginator.page(page)
    except PageNotAnInteger:
        list_page = paginator.page(1)
    except EmptyPage:
        list_page = paginator.page(paginator.num_pages)
    return render(request, 'blog/index.html', context={'post_list': list_page,
                                                    "is_paginated": is_page})


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


