#!/usr/bin/env python
#-*- coding:utf-8 -*-
from django.http.response import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import F
import json
# from django.utils import simplejson as json


from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from django.core.paginator import Paginator, InvalidPage, EmptyPage

from django.utils import timezone

from blog.models import Blog, Tag, Category, Link, User, Comment,UserVisitFoot
from forms import CommentForm, FeedBackForm
import random

from django.core.mail import send_mail

from utils import get_user_device, get_user_ip

def save_user_visitfoot(request):
    ip = get_user_ip(request)
    print ip
    try:
        userfoot = UserVisitFoot.objects.get(userIP = ip)
    except:
        userfoot = UserVisitFoot(userIP = ip)

    userfoot.save()

def home(request):
    device  = get_user_device(request)
    # save_user_visitfoot(request) # 保存用户足迹
    template = 'blog/home.html' if device == 'PC' else 'blog/mobile/home.mobile.html'
    context = {}
    return render_to_response(template, context,
                              context_instance=RequestContext(request))

def index(request,page=1):
    device  = get_user_device(request)
    template = 'blog/blog.html' if device == 'PC' else 'blog/mobile/blog.mobile.html'

    blog_list   = Blog.objects.all().order_by('-publish_time')
    paginator   = Paginator(blog_list,5)

    try :
        page    = int(request.GET.get('page','1'))
    except ValueError:
        page    = 1

    try :
        blogs   = paginator.page(page)
    except (EmptyPage, InvalidPage):
        blogs   = paginator.page(paginator.num_pages)



    newblogs    = Blog.objects.all().order_by('-publish_time')[0:8]
    categorys   = Category.objects.all()
    reads       = Blog.objects.filter(read_num__gt = 0).order_by('-read_num')[0:8]
    comments    = Blog.objects.filter(comment_num__gt = 0).order_by('-comment_num')[0:8]
    links       = Link.objects.all()
    context     = {'blogs':blogs,'newblogs':newblogs,'categorys':categorys,
                   'reads':reads,'comments':comments,'links':links, 'SHOWSHORTBLOG':'True'}
    return render_to_response(template, context,
                              context_instance=RequestContext(request))

# class IndexView(generic.ListView):
#     template_name           = 'blog.html'
#     context_object_name     = 'blogs'


def detail(request, blog_id):
    # print blog_id
    device  = get_user_device(request)
    template = 'blog/detail.html' if device == 'PC' else 'blog/mobile/detail.mobile.html'

    categorys   = Category.objects.all()
    form        = CommentForm()
    blog            = Blog.objects.get(id=blog_id)
    blog.read_num  += 1
    blog.save()
    comments    = Comment.objects.filter(blog = blog)
    # blog            = Blog.objects.get(pk=blog_id)
    try :
        pre_blog = Blog.objects.filter(publish_time__lt = blog.publish_time).order_by('-publish_time')[0]
    except :
        pre_blog = None
    try :
        next_blog = Blog.objects.filter(publish_time__gt = blog.publish_time).order_by('publish_time')[0]
    except :
        next_blog = None
    return render_to_response(template, {'blog':blog,'pre_blog':pre_blog,'categorys':categorys,
                                                  'next_blog':next_blog,'form':form,
                                                  'comments':comments},
                        context_instance=RequestContext(request))

def catelist(request,cate_id):

    device  = get_user_device(request)
    template = 'blog/blog.html' if device == 'PC' else 'blog/mobile/blog.mobile.html'

    blog_list   = Blog.objects.filter(category = cate_id)
    paginator   = Paginator(blog_list,5)

    try :
        page    = int(request.GET.get('page','1'))
    except ValueError:
        page    = 1

    try :
        blogs   = paginator.page(page)
    except (EmptyPage, InvalidPage):
        blogs   = paginator.page(paginator.num_pages)

    newblogs    = Blog.objects.all().order_by('-publish_time')[0:8]
    categorys   = Category.objects.all()
    reads       = Blog.objects.filter(read_num__gt = 0).order_by('-read_num')[0:8]
    comments    = Blog.objects.filter(comment_num__gt = 0).order_by('-comment_num')[0:8]
    links       = Link.objects.all()
    context     = {'blogs':blogs,'newblogs':newblogs,'categorys':categorys,
                   'reads':reads,'comments':comments,'links':links, 'SHOWSHORTBLOG':'True'}
    return render_to_response(template,context,
                              context_instance=RequestContext(request))


def taglist(request, tag_id):

    device  = get_user_device(request)
    template = 'blog/blog.html' if device == 'PC' else 'blog/mobile/blog.mobile.html'

    blog_list   = Blog.objects.filter(tags = tag_id)
    paginator   = Paginator(blog_list,5)

    try :
        page    = int(request.GET.get('page',1))
    except ValueError:
        page    = 1

    try :
        blogs   = paginator.page(page)
    except (EmptyPage, InvalidPage):
        blogs   = paginator.page(paginator.num_pages)

    newblogs    = Blog.objects.all().order_by('-publish_time')[0:8]
    categorys   = Category.objects.all()
    reads       = Blog.objects.filter(read_num__gt = 0).order_by('-read_num')[0:8]
    comments    = Blog.objects.filter(comment_num__gt = 0).order_by('-comment_num')[0:8]
    links       = Link.objects.all()
    context     = {'blogs':blogs,'newblogs':newblogs,'categorys':categorys,
                   'reads':reads,'comments':comments,'links':links, 'SHOWSHORTBLOG':'True'}
    return render_to_response(template, context,
                              context_instance=RequestContext(request))
def DeleteHeadBlank(s):
    for i in xrange(len(s)):
        if s[i] not in [' ','   ']:
            return s[i:]
def ResponseMsg(status,errorMsg):
    reJson = {}
    reJson['status'] = status
    reJson['errorMsg'] = errorMsg
    return HttpResponse(json.dumps(reJson),content_type='application/json')
def comment(request):

    if request.is_ajax():
            form = CommentForm(request.POST)

            if form.is_valid():
                blog_id     = request.GET.get('blog_id')
                blog        = get_object_or_404(Blog, pk = blog_id)
                blog.comment_num += 1
                blog.save()
                pre_comid   = form.cleaned_data['pre_comid']
                nickname    = form.cleaned_data['anickname']

                email       = form.cleaned_data['bemail']
                website     = form.cleaned_data['cwebsite']
                content     = form.cleaned_data['dcontent']
                photo       = str(random.randint(0,9))+'.png'
                u = User (name=nickname, email=email, website=website,photo=photo)
                u.save()
                # sendCommentReply(email,content)
                c = Comment(user=u,blog=blog,content=content,comment_time=timezone.now())
                c.save()
                return ResponseMsg(True,u'谢谢你的评论')
            else:
               return ResponseMsg(False,form.errors.popitem()[1])
    else:
        raise Http404

# def commentold(request):
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             return HttpResponse(form.cleaned_data)
#     else:
#         form = CommentForm()
#
#     return render_to_response('blog/comment.html',{'form':form},
#                               context_instance=RequestContext(request))

def sendCommentReply(email, content):
    SERVER_EMAIL    = ''
    title           = u''
    content         = u''+content
    send_mail(title, content, SERVER_EMAIL, [email])

# 关于
def about(request):

    device  = get_user_device(request)
    template = 'blog/about.html' if device == 'PC' else 'blog/mobile/about.mobile.html'

    form    = FeedBackForm()
    return render_to_response(template,{'form':form},
                              context_instance=RequestContext(request))

def feedback(request):
    
    if request.is_ajax():
            form = FeedBackForm(request.POST)
            if form.is_valid():
                feedback = form.save(commit=False)
                feedback.save()
                return ResponseMsg(True,u'感谢你的反馈建议.我会及时进行改进.')
            else:
               return ResponseMsg(False,form.errors.popitem()[1])
    else:
        raise Http404