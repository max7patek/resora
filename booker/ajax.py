
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import Context, loader
from django.db import transaction
from django.contrib.auth.decorators import login_required

from booker.models import *
from booker.authorization import *

from users.models import User

import datetime
import booker.patches






@login_required
def all_bookables(request):
    template = loader.get_template('booker/bookables-ajax.html')
    bookables = Bookable.objects.all()
    times = sorted(set(map(lambda i: i.starttime, bookables)))
    availabilities = map(Bookable.any_available_at_time, times)
    context = {
        'no_bookables' : len(times) == 0,
        'times_isos_and_availabilities' : zip(times, map(datetime.datetime.isoformat, times), availabilities),
    }
    return HttpResponse(template.render(context, request))

@login_required
def booked(request):
    if request.user.user.booking is not None:
        return JsonResponse({'booked':True})
    else:
        return JsonResponse({'booked':False})

@login_required
def bookings(request):
    if not is_ta(request.user.email):
        template = loader.get_template('booker/mustbeta-ajax.html')
        return HttpResponse(template.render({'email':request.user.email}, request))
    template = loader.get_template('booker/bookings-ajax.html')
    bookables = sorted(Bookable.objects.all(), key=lambda i: i.starttime)
    if len(bookables) == 0:
        rows = []
    else:
        rows = [[bookables[0]]]
        for i in range(1, len(bookables)):
            if bookables[i].starttime == bookables[i-1].starttime:
                rows[-1].append(bookables[i])
            else:
                rows.append([bookables[i]])

    context = {
        'rows':zip(rows, map(lambda i: i[0].starttime, rows)),
    }
    return HttpResponse(template.render(context, request))


@login_required
def book(request):
    if not is_enrolled(request.user.email):
        return JsonResponse({
            'error': True,
            'message': 'Must be enrolled to book office hours.',
        })
    time = datetime.datetime.fromisoformat(request.GET.get('time'))
    with transaction.atomic():
        bookables = Bookable.objects.select_for_update().filter(starttime=time)
        for b in bookables:
            if b.available():
                request.user.user.booking = b
                request.user.user.save()
                return JsonResponse({
                    'error': False,
                    'message': 'Successfully booked!',
                })
        else:
            return JsonResponse({
                'error': True,
                'message': 'No available bookables at this time.',
            })

@login_required
def release_booking(request):
    with transaction.atomic():
        usr = User.objects.select_for_update().get(pk=request.user.user.pk)
        usr.booking = None
        usr.save()
    return JsonResponse({})
