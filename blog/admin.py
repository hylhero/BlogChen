#!/usr/bin/env python
#-*- coding:utf-8 -*-
from django.contrib import admin

# 2014-7-3 17:00 by cheer
from blog.models import Tag, Category, User, Blog, Link, Comment, UploadFileModel

class UserAdmin(admin.ModelAdmin):
    list_display        = ('name','email','website','photo','sex')
    search_field        = ('name',)
    list_per_page       = 10

class BlogAdmin(admin.ModelAdmin):
    list_display        = ('title','publish_time','update_time',
                            'category','read_num','comment_num')
    list_filter         = ('publish_time',)
    date_hierarchy      = 'publish_time'
    ordering            = ('-publish_time',)
    filter_horizontal   = ('tags',)
    list_per_page       = 10

class LinkAdmin(admin.ModelAdmin):
    list_display        = ('site_name','site_url','site_description',)
    list_per_page       = 10

class CommentAdmin(admin.ModelAdmin):
    list_display        = ('id','user','blog','content','comment_time','pre_com')
    list_per_page       = 10

class UploadFileAdmin(admin.ModelAdmin):
    list_display        = ('id','filename','filetype','filesize','filepath','uploaddate')
    list_per_page       = 10




admin.site.register(User, UserAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(UploadFileModel, UploadFileAdmin)