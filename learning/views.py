from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from learning import models
import json
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def login(request):
    if request.method == 'POST':
        r = models.Feed.objects.get(pk=1)
        return HttpResponse(request.POST['name'])
    if request.method == 'DELETE':
        return HttpResponse('delete')
    if request.method == 'GET':
        return JsonResponse({'method': 'get'})


def register(request):
    return HttpResponse("Registracia")


def inzeraty_id(request, inzerat_id):
    try:
        inz = models.Feed.objects.get(pk=inzerat_id)
        inz = dict(inz.objects.values())
        return JsonResponse(inz, safe=False, status=200)
    except models.Feed.DoesNotExist:
        return HttpResponseNotFound("Inzerat s tymto id neexistuje")


def inzeraty_all(request):
   # inz = models.Feed.objects.get(pk=inzerat_id)
    # inz = dict(inz.objects.values())
    inzs = list(models.Feed.objects.values())
    return JsonResponse(inzs, safe=False, status=200)

def users_id(request, user_id):

    user = dict(models.Users.objects.values())
    return JsonResponse(user, safe=False, status=200)


def list(request):
    if request.method == 'GET':
        data = serializers.serialize('json', models.Feed.objects.all())
        return HttpResponse(data, status=200)
    return JsonResponse(status=401)

