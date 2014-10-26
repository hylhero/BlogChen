# -*- coding:utf-8 -*-

from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from blog.models import Blog


class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Blog.objects.all()

    def lastmod(self, obj):
        return obj.update_time

    def location(self, obj):
        return reverse('blog:detail', args=[obj.id])
