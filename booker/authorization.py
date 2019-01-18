
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from booker.models import *



def is_ta(email):
    return TA.objects.filter(email=email.lower()).exists()


def is_enrolled(email):
    return Student.objects.filter(email=email.lower()).exists()
