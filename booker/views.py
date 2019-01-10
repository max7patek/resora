from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import Context, loader
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.core.management import call_command


from booker.models import *
from booker.authorization import *
from booker.forms import *

from collections import Counter

# Create your views here.

@login_required
def bookables(request):
    if is_ta(request.user.email):
        return HttpResponseRedirect('ta')
    if request.user.user.booking is not None:
        return HttpResponseRedirect('booking')
    template = loader.get_template('booker/bookables.html')
    calendars = []
    for cal in Calendar.objects.all():
        gcal_id = cal.gcal_id
        calendars.append(gcal_id.split('@')[0])
    return HttpResponse(template.render({'calendars':calendars}, request))

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
    if not is_ta(request.user.email):
        return HttpResponseRedirect('/bookables')
    template = loader.get_template('booker/ta.html')
    return HttpResponse(template.render({'form':UploadRosterForm()}, request))

@login_required
def manual_pull(request):
    if not is_ta(request.user.email):
        return HttpResponseRedirect('/bookables')
    if request.method == 'POST':
        call_command('pullofficehours', request.POST.get('hours'))
    return HttpResponseRedirect('/ta')

@login_required
def roster_upload(request):
    if not is_ta(request.user.email):
        return HttpResponseRedirect('/bookables')
    if request.method == 'POST':
        form = UploadRosterForm(request.POST, request.FILES)
        if form.is_valid():
            UploadRosterForm.handle_uploaded_file(request.FILES['file'], request.POST.get('override'))
            return HttpResponseRedirect('/ta')
    else:
        form = UploadRosterForm()
    return HttpResponseRedirect('/ta')

def landing(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('bookables')
    template = loader.get_template('booker/landing.html')
    return HttpResponse(template.render({}, request))
