# -*- coding:utf-8 -*-
from django.contrib.syndication.views import Feed
from blog.models import Blog
from blog.templatetags.filters import shortblog


class LatestBlogFeed(Feed):

    title = u'd9chen的博客'
    link = '/blog/rss/'
    author = 'cheer'
    description = u'关注Python django sublime web开发'

    def items(self):
        return Blog.objects.all().order_by('-publish_time')[:8]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return shortblog(item.content, 8)

    def item_pubdate(self, item):
        return item.publish_time

    def item_link(self, item):
        return '/blog/detail/{0}'.format(item.id)
