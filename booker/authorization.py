
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from booker.models import *

# TODO Improve this lol

def is_ta(email):
    return len(TA.objects.filter(email=email)) > 0


def is_enrolled(email):
    return len(Student.objects.filter(email=email)) > 0
