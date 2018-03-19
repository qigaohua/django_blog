# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from .forms import CommentForm


# Create your views here.
def post_comment(request, pk_post):
    post = get_object_or_404(Post, pk=pk_post)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            html = '/post/%s/' % pk_post
            return redirect(html)
        else:
            comment_list = Post.comment_set.all()
            context = {'post': post, 'form': form, 'comment_list': comment_list}

            return render(request, 'blog/detail.html', context=context)

    html = '/post/%s/' % pk_post
    return redirect(html)
