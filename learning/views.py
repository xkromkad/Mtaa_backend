from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Feed, Chats
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@csrf_exempt
def login(request):
    if request.method == 'POST':
        r = Feed.objects.get(pk=1)
        return HttpResponse(request.POST['name'])
    if request.method == 'DELETE':
        return HttpResponse('delete')
    if request.method == 'GET':
        return JsonResponse({'method': 'get'})


def register(request):
    return HttpResponse("Registracia")


def inzeraty_id(request, inzerat_id):
    return HttpResponse(f"Inzerat {inzerat_id}")


def users_id(request, user_id):
    return HttpResponse(f"Pouzivatel {user_id}")


def list(request):
    if request.method == 'GET':
        data = serializers.serialize('json', Feed.objects.all())
        return HttpResponse(data, status=200)
    return JsonResponse(status=401)
