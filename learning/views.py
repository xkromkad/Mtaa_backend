from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from learning import models
import json
from django.http import JsonResponse
from learning import serializers
from django.forms.models import model_to_dict


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def login(request):
    if request.method == 'POST':
        r = models.Feed.objects.all()
        return HttpResponse(request.POST['name'])
    if request.method == 'DELETE':
        return HttpResponse('delete')
    if request.method == 'GET':
        return JsonResponse({'method': 'get'})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        i = 0
        while 1:
            i += 1
            try:
                one_user = models.Users.objects.get(pk=i)
            except models.Users.DoesNotExist:
                break
        serializer = serializers.UserSerializer(data=json.loads(request.body))
        if serializer.is_valid():
            serializer.id = i
            person = serializer.save()
            registered_data = {'id': person.id, 'email': person.email, 'message': "pouzivatel bol uspesne vytvoreny"}
        else:
            registered_data = serializer.errors

        return JsonResponse(registered_data, safe=False, status=200)


def inzeraty_id(request, inzerat_id):
    if request.method == 'GET':
        try:
            inz = models.Feed.objects.get(pk=inzerat_id)
            inz = dict(inz.objects.values())
            return JsonResponse(inz, safe=False, status=200)
        except models.Feed.DoesNotExist:
            return HttpResponseNotFound("Inzerat s tymto id neexistuje")

"""
def inzeraty_all(request):
   # inz = models.Feed.objects.get(pk=inzerat_id)
    # inz = dict(inz.objects.values())
    inzs = list(models.Feed.objects.values())
    return JsonResponse(inzs, safe=False, status=200)
"""


def users_id(request, user_id):
    if request.method == 'GET':
        try:
            userik = models.Users.objects.get(pk=user_id)
            valuees = {"name": userik.name, "email": userik.email,"photo":userik.photo}
            return JsonResponse(valuees, safe=False, status=200)
        except models.Users.DoesNotExist:
            return HttpResponseNotFound("Pouzivatel s tymto id neexistuje")


"""
def list(request):
    if request.method == 'GET':
        data = serializers.serialize('json', models.Feed.objects.all())
        return HttpResponse(data, status=200)
    return JsonResponse(status=401)

"""