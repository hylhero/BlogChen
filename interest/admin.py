# -*- coding: utf-8 -*-
from django.contrib import admin

from models import ActorModel, AreaModel, MovieStyleModel, MovieModel

class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'area', 'img')
    search_fields = ('name',)
    list_per_page = 20
    ordering = ('-createdate',)
    filter_horizontal = ('style', 'actors')


admin.site.register(MovieModel, MovieAdmin)
admin.site.register(AreaModel)
admin.site.register(ActorModel)
admin.site.register(MovieStyleModel)


