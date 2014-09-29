# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http.response import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from interest.models import Movie, MovieStyle, Actor, Area

def movieIndex(request):
    movies = Movie.objects.all().order_by('-createdate')
    template = 'interest/movie.html'
    context ={'movies':movies,}
    return render_to_response(template, context, context_instance=RequestContext(request))
