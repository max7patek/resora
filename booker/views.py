from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader

from booker.models import *

from collections import Counter


# Create your views here.

def main(request):
    # TODO: direct to users booking if has one
    template = loader.get_template('booker/main.html')
    context = {}
    return HttpResponse(template.render(context, request))

def all_bookables(request):
    template = loader.get_template('booker/bookables.html')
    bookables = Bookable.objects.all()
    context = {
        'bookables' : zip(
            bookables,
            (hasattr(b, 'booker') and b.booker is not None for b in bookables)), # booked
    }
    return HttpResponse(template.render(context, request))

def as_ta(request):
    template = loader.get_template('booker/ta.html')
    context = {}
    return HttpResponse(template.render(context, request))

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


def book(request):
    pk = request.GET.get('bookable')
    bookable = Bookable.objects.get(pk=pk)
    request.user.user.book(bookable)
    return HttpResponseRedirect('')


def release_booking(request):
    request.user.user.release_booking()
    return HttpResponseRedirect('')
