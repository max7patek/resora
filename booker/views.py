from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import Context, loader
from django.db import transaction
from django.contrib.auth.decorators import login_required

from booker.models import *

from collections import Counter

def ta_required(func):
    def wrapper(request, *args, **kwargs):
        if len(TA.objects.filter(email=request.user.email)) > 0:
            return func(request, *args, **kwargs)
        else:
            template = loader.get_template('booker/must_be_ta.html')
            return HttpResponse(template.render({'email':request.user.email}, request))
    return wrapper


# Create your views here.

def main(request):
    # TODO: direct to users booking if has one
    template = loader.get_template('booker/main.html')
    context = {}
    return HttpResponse(template.render(context, request))

@login_required
def all_bookables(request):
    template = loader.get_template('booker/bookables.html')
    bookables = Bookable.objects.all()
    context = {
        'bookables' : zip(
            bookables,
            (hasattr(b, 'booker') and b.booker is not None for b in bookables)), # booked
    }
    return HttpResponse(template.render(context, request))

@login_required
def as_ta(request):
    template = loader.get_template('booker/ta.html')
    context = {}
    return HttpResponse(template.render(context, request))

@login_required
@ta_required
def bookings(request):
    template = loader.get_template('booker/bookings.html')
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
