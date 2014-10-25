#!/usr/bin/env python
#-*- coding:utf-8 -*-
from django.http.response import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import F
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils import timezone
from blog.models import Blog, Tag, Category, Link, User, Comment, UserVisitFoot
from forms import CommentForm, FeedBackForm
from django.core.mail import send_mail
from utils import get_user_device, get_user_ip
from django.views.generic.base import TemplateResponseMixin, View
import re
import random
import json


def save_user_visitfoot(request):
    ip = get_user_ip(request)
    print ip
    try:
        userfoot = UserVisitFoot.objects.get(userIP=ip)
    except:
        userfoot = UserVisitFoot(userIP=ip)

    userfoot.save()


def DeleteHeadBlank(s):
    for i in xrange(len(s)):
        if s[i] not in [' ', '   ']:
            return s[i:]


def ResponseMsg(status, errorMsg):
    reJson = {}
    reJson['status'] = status
    reJson['errorMsg'] = errorMsg
    return HttpResponse(json.dumps(reJson), content_type='application/json')


def comment(request):
    if request.is_ajax():
            form = CommentForm(request.POST)

            if form.is_valid():
                blog_id = request.GET.get('blog_id')
                blog = get_object_or_404(Blog, pk=blog_id)
                blog.comment_num += 1
                blog.save()
                pre_comid = form.cleaned_data['pre_comid']
                nickname = form.cleaned_data['anickname']

                email = form.cleaned_data['bemail']
                website = form.cleaned_data['cwebsite']
                content = form.cleaned_data['dcontent']
                photo = str(random.randint(0, 9)) + '.png'
                u = User(name=nickname, email=email, website=website, photo=photo)
                u.save()
                c = Comment(user=u, blog=blog, content=content, comment_time=timezone.now())
                c.save()
                # sendCommentReply(email)
                # SendEmail_Comment(nickname,None)
                return ResponseMsg(True, u'谢谢你的评论')
            else:
               return ResponseMsg(False, form.errors.popitem()[1])
    else:
        raise Http404


def feedback(request):
    if request.is_ajax():
            form = FeedBackForm(request.POST)
            if form.is_valid():
                feedback = form.save(commit=False)
                feedback.save()
                return ResponseMsg(True, u'感谢你的反馈建议.我会及时进行改进.')
            else:
               return ResponseMsg(False, form.errors.popitem()[1])
    else:
        raise Http404


user_device_re = re.compile(r'(mobile|iphone|android|iemobile)')


class BlogBase(TemplateResponseMixin, View):
    template_name = ''
    template_name_m = ''

    def get_user_device(self):
        # return 'MOBILE'
        device = self.request.session.get('USER_VIEW_DEVICE', 'UNKNOWN_VIEW_DEVICE')
        if device != 'UNKNOWN_VIEW_DEVICE':
            return device

        HTTP_USER_AGENT = self.request.META.get('HTTP_USER_AGENT', '').lower()
        user_device = user_device_re.findall(HTTP_USER_AGENT)
        if len(user_device) > 0:
            self.request.session['USER_VIEW_DEVICE'] = 'MOBILE'
            return 'MOBILE'

        self.request.session['USER_VIEW_DEVICE'] = 'PC'
        return 'PC'

    def get_template_names(self):
        if self.get_user_device() == 'MOBILE':
            return [self.template_name_m]
        else:
            return [self.template_name]

    def get_context_data(self, extra_context):
        context = {
            'newblogs': Blog.objects.all().order_by('-publish_time')[0:8],
            'categorys': Category.objects.all(),
            'reads': Blog.objects.filter(read_num__gt=0).order_by('-read_num')[0:8],
            'comments': Blog.objects.filter(comment_num__gt=0).order_by('-comment_num')[0:8],
            'links': Link.objects.all(),
        }
        context.update(extra_context)
        return context


class Home(BlogBase):
    template_name = 'blog/home.html'
    template_name_m = 'blog/mobile/home.mobile.html'

    def get_context_data(self, extra_context):
        context = super(Home, self).get_context_data(extra_context)
        return context

    def get(self, request):

        print 'BlogHome View'
        extra_context = {
        }
        return self.render_to_response(self.get_context_data(extra_context))


class BlogIndex(BlogBase):
    template_name = 'blog/blog.html'
    template_name_m = 'blog/mobile/blog.mobile.html'

    def get_context_data(self, extra_context):
        context = super(BlogIndex, self).get_context_data(extra_context)
        return context

    def get(self, request):
        print 'BlogIndex'
        blog_list = Blog.objects.all().order_by('-publish_time')
        paginator = Paginator(blog_list, 5)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1

        try:
            blogs = paginator.page(page)
        except (EmptyPage, InvalidPage):
            blogs = paginator.page(paginator.num_pages)
        extra_context = {
            'SHOWSHORTBLOG': 'True',
            'blogs': blogs,
        }
        return self.render_to_response(self.get_context_data(extra_context))


class BlogDetail(BlogBase):
    template_name = 'blog/detail.html'
    template_name_m = 'blog/mobile/detail.mobile.html'

    def get_context_data(self, extra_context):
        context = super(BlogDetail, self).get_context_data(extra_context)
        return context

    def get(self, request, blog_id):
        print 'BlogDetail'
        blog = Blog.objects.get(id=blog_id)
        blog.read_num += 1
        blog.save()
        try:
            pre_blog = Blog.objects.filter(publish_time__lt=blog.publish_time).order_by('-publish_time')[0]
        except:
            pre_blog = None
        try:
            next_blog = Blog.objects.filter(publish_time__gt=blog.publish_time).order_by('publish_time')[0]
        except:
            next_blog = None
        extra_context = {
            'SHOWSHORTBLOG': 'False',
            'blog': blog,
            'form': CommentForm(),
            'comments': Comment.objects.filter(blog=blog),
            'pre_blog': pre_blog,
            'next_blog': next_blog,
        }
        return self.render_to_response(self.get_context_data(extra_context))


class BlogCate(BlogBase):
    template_name = 'blog/blog.html'
    template_name_m = 'blog/mobile/blog.mobile.html'

    def get_context_data(self, extra_context):
        context = super(BlogCate, self).get_context_data(extra_context)
        return context

    def get(self, request, cate_id):
        print 'BlogCate'
        blog_list = Blog.objects.filter(category=cate_id)
        paginator = Paginator(blog_list, 5)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try:
            blogs = paginator.page(page)
        except (EmptyPage, InvalidPage):
            blogs = paginator.page(paginator.num_pages)
        extra_context = {
            'SHOWSHORTBLOG': 'True',
            'blogs': blogs,
        }
        return self.render_to_response(self.get_context_data(extra_context))


class BlogTag(BlogBase):
    template_name = 'blog/blog.html'
    template_name_m = 'blog/mobile/blog.mobile.html'

    def get_context_data(self, extra_context):
        context = super(BlogTag, self).get_context_data(extra_context)
        return context

    def get(self, request, tag_id):
        print 'BlogCate'
        blog_list = Blog.objects.filter(tags=tag_id)
        paginator = Paginator(blog_list, 5)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try:
            blogs = paginator.page(page)
        except (EmptyPage, InvalidPage):
            blogs = paginator.page(paginator.num_pages)
        extra_context = {
            'SHOWSHORTBLOG': 'True',
            'blogs': blogs,
        }
        return self.render_to_response(self.get_context_data(extra_context))


class About(BlogBase):
    template_name = 'blog/about.html'
    template_name_m = 'blog/mobile/about.mobile.html'

    def get_context_data(self, extra_context):
        context = super(About, self).get_context_data(extra_context)
        return context

    def get(self, request):
        print 'About'
        extra_context = {
            'form': FeedBackForm(),
        }
        return self.render_to_response(self.get_context_data(extra_context))
