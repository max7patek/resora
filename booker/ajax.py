
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import Context, loader
from django.db import transaction
from django.contrib.auth.decorators import login_required

from booker.models import *
from booker.authorization import *



@login_required
def all_bookables(request):
    template = loader.get_template('booker/bookables-ajax.html')
    bookables = Bookable.objects.all()
    context = {
        'no_bookables' : len(Bookable.objects.all()) == 0,
        'bookables' : zip(
            bookables,
            (hasattr(b, 'booker') and b.booker is not None for b in bookables)), # booked
    }
    return HttpResponse(template.render(context, request))


@login_required
@ta_required
def bookings(request):
    template = loader.get_template('booker/bookings-ajax.html')
    bookables = sorted(Bookable.objects.all(), key=lambda i: i.starttime)
    if len(bookables) == 0:
        rows = []
    else:
        rows = [[bookables[0]]]
        for i in range(1, len(bookables)):
            if bookables[i].starttime == bookables[i-1]:
                rows[-1].append(bookables[i])
            else:
                rows.append([bookables[i]])

    context = {
        'rows':zip(rows, map(lambda i: i[0].starttime, rows)),
    }
    return HttpResponse(template.render(context, request))


@login_required
def book(request):
    pk = request.GET.get('bookable')
    with transaction.atomic():
        try:
            bookable = Bookable.objects.select_for_update().get(pk=pk)
            if hasattr(bookable, 'booker') and bookable.booker is not None:
                return JsonResponse({
                    'result': 'Bookable has already been booked'
                })
            request.user.user.book(bookable)
        except Bookable.DoesNotExist:
            return JsonResponse({
                'result': 'Bookable does not exist'
            })
    return JsonResponse({
        'result': 'success'
    })

@login_required
def release_booking(request):
    request.user.user.release_booking()
    return JsonResponse({})
