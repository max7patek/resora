
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from booker.models import *

def is_ta(email):
    return len(TA.objects.filter(email=email)) > 0


def ta_required(func):
    """should only wrap views that return HttpResponse"""
    def wrapper(request, *args, **kwargs):
        if is_ta(request.user.email) > 0:
            return func(request, *args, **kwargs)
        else:
            template = loader.get_template('booker/mustbeta-ajax.html')
            return HttpResponse(template.render({'email':request.user.email}, request))
    return wrapper
