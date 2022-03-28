from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from learning import models
import json
from django.core import serializers
from django.utils import timezone

# todo:
# Registrácia s uložením do db
# login
# autorizácia cez tokeny
# posielanie fotky
# vytvorenie chatu
# vytvorenie chat group
# pridanie súboru k inzerátu, posielanie súborov
# vytvoriť swagger
# aktualizácia dokumentácie

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
def reg(request):
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

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data['email'] == models.Users.objects.filter(email=data['email']).first().email:
            return HttpResponse('Already used email '+data['email'], status=405)
        models.Users(name = data['name'],
                     surname = data['surname'],
                     email = data['email'],
                     password = data['password'],
                     photo = data['photo'],
                     created_at = timezone.now(),
                     updated_at = timezone.now()).save()
        return HttpResponse(status=200)

@csrf_exempt
def inzeraty_id(request, inzerat_id):
    if request.method == 'GET':
        try:
            inz = models.Feed.objects.get(pk=inzerat_id)
            inz = dict(inz.objects.values())
            return JsonResponse(inz, safe=False, status=200)
        except models.Feed.DoesNotExist:
            return HttpResponseNotFound("Inzerat s tymto id neexistuje")
    if request.method == 'DELETE':
        models.Feed.objects.filter(pk=inzerat_id).first().delete()
        return HttpResponse(status=204)
    if request.method == 'PUT':
        model = models.Feed.objects.filter(pk=inzerat_id).first()
        data = json.loads(request.body)
        if 'title' in data:
            model.title = data['title']
        if 'description' in data:
            model.description = data['description']
        model.save()
        return HttpResponse(status=200)

"""
{
    "title": "Python programming",
    "description": "Chcel by som vedieť cykly a funkcie."
}
"""

"""
def inzeraty_all(request):
   # inz = models.Feed.objects.get(pk=inzerat_id)
    # inz = dict(inz.objects.values())
    inzs = list(models.Feed.objects.values())
    return JsonResponse(inzs, safe=False, status=200)
"""

@csrf_exempt
def users_id(request, user_id):
    if request.method == 'GET':
        try:
            userik = models.Users.objects.get(pk=user_id)
            valuees = {"name": userik.name, "email": userik.email,"photo":userik.photo}
            return JsonResponse(valuees, safe=False, status=200)
        except models.Users.DoesNotExist:
            return HttpResponseNotFound("Pouzivatel s tymto id neexistuje")
    if request.method == 'PUT':
        model = models.Users.objects.filter(pk=user_id).first()
        print(model)
        data = json.loads(request.body)
        if 'name' in data:
            model.name = data['name']
        if 'surname' in data:
            model.surname = data['surname']
        if 'email' in data:
            model.email = data['email']
        if 'password' in data:
            model.password = data['password']
        if 'photo' in data:
            model.photo = data['photo']
        model.save()
        return HttpResponse(status=200)
    if request.method == 'DELETE':
        models.Users.objects.filter(pk=user_id).first().delete()
        return HttpResponse(status=204)

{
    "name": "Martin",
    "surname": "Nejaký"
}


@csrf_exempt
def inzeraty_list(request):
    if request.method == 'GET':
        data = serializers.serialize('json', models.Feed.objects.all())
        return HttpResponse(data, status=200)
    if request.method == 'POST':
        data = json.loads(request.body)
        models.Feed(title = data['title'],
                    description = data['description'],
                    created_at = timezone.now(),
                    updated_at = timezone.now(),
                    user = models.Users.objects.first()).save()
        return HttpResponse(status=200)
    return HttpResponse(status=401)

# posielam v post na /inzeraty
'''
{
    "title": "Pravdepodobnosť",
    "description": "Chcel by som sa naučiť kombinácie s opakovaním."
}
'''

