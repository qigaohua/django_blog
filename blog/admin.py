# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from blog.models import Category, Tag, Post


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'auther', 'modified_time')
    search_fields = ('title', )
    list_filter = ('modified_time',)
    # date_hierarchy = 'modified_time'
    filter_horizontal = ('tags', )


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
