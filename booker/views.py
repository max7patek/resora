from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import Context, loader
from django.db import transaction
from django.contrib.auth.decorators import login_required

from booker.models import *
from booker.authorization import *

from collections import Counter

# Create your views here.

@login_required
def bookables(request):
    if is_ta(request.user.email):
        return HttpResponseRedirect('ta')
    if request.user.user.booking is not None:
        return HttpResponseRedirect('booking')
    template = loader.get_template('booker/bookables.html')
    return HttpResponse(template.render({}, request))

@login_required
def booking(request):
    if is_ta(request.user.email):
        return HttpResponseRedirect('ta')
    if request.user.user.booking is None:
        return HttpResponseRedirect('bookables')
    template = loader.get_template('booker/booking.html')
    return HttpResponse(template.render({}, request))

@login_required
def as_ta(request):
    template = loader.get_template('booker/ta.html')
    return HttpResponse(template.render({}, request))

def landing(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('bookables')
    template = loader.get_template('booker/landing.html')
    return HttpResponse(template.render({}, request))
