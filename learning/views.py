import os
import uuid
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from learning import models
import json
from django.core import serializers
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# todo:
# login
# autorizácia cez tokeny
# posielanie fotky
# pridanie súboru k inzerátu, posielanie súborov
# vytvoriť swagger
# aktualizácia dokumentácie

@csrf_exempt
def login(request):
    if request.method == 'POST':
        permission_classes = (IsAuthenticated,)
        return HttpResponse('ahoj')

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
        data = json.loads(request.POST['req'])
        email = models.Users.objects.filter(email=data['email']).first()
        if email is not None and data['email'] == email.email:
            return HttpResponse('Already used email '+data['email'], status=405)
    if request.FILES.get("image", None) is None:
        return HttpResponse(status=400)
    img = request.FILES["image"]
    img_extension = os.path.splitext(img.name)[1]
    save_path = "learning/images"
    img_name = str(uuid.uuid4())
    img_save_path = "%s/%s%s" % (save_path, img_name, img_extension)
    with open(img_save_path, "wb+") as f:
        for chunk in img.chunks():
            f.write(chunk)
        models.Users(name = data['name'],
                     surname = data['surname'],
                     email = data['email'],
                     password = data['password'],
                     photo = img_name+img_extension,
                     created_at = timezone.now(),
                     updated_at = timezone.now()).save()
        return HttpResponse(status=200)

@csrf_exempt
def inzeraty_id(request, inzerat_id):
    if request.method == 'GET':
        if models.Files.objects.filter(feed=inzerat_id) is not None:
            files = models.Files.objects.filter(feed=inzerat_id)
            file_arr = []
            for item in files:
                with open('learning/files/{0}'.format(item.file_name), "rb") as f:
                    file = f.read()
                    file_type = os.path.splitext('321bc5cc-7ac4-450a-af5d-1263dc4cedc9.jpg')[1]
                    file_arr.append([file, file_type])
        try:
            model = models.Feed.objects.filter(pk=inzerat_id)
            data = serializers.serialize("json", model)
            return HttpResponse([file_arr, data], status=200)
        except models.Feed.DoesNotExist:
            return HttpResponseNotFound("Inzerat s tymto id neexistuje")
    if request.method == 'DELETE':
        model = models.Feed.objects.filter(pk=inzerat_id).first()
        try:
            os.remove("learning/images/{0}".format(model.photo))
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
        model.delete()
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
        data = json.loads(request.POST['content'])
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
        data = json.loads(request.POST['content'])
        model = models.Feed(title = data['title'],
                    description = data['description'],
                    created_at = timezone.now(),
                    updated_at = timezone.now(),
                    user = models.Users.objects.first())
        model.save()
        if request.FILES.get("file", None) is not None:
            for file in request.FILES.getlist('file'):
                extension = os.path.splitext(file.name)[1]
                save_path = "learning/files"
                name = str(uuid.uuid4())
                save_path = "%s/%s%s" % (save_path, name, extension)
                with open(save_path, "wb+") as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                models.Files(file_name=name+extension,
                             feed=model).save()
        return HttpResponse(status=200)
    return HttpResponse(status=401)

# posielam v post na /inzeraty
'''
{
    "title": "Pravdepodobnosť",
    "description": "Chcel by som sa naučiť kombinácie s opakovaním."
}
'''

