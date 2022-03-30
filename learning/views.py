import os
import uuid
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView
from rest_framework import viewsets

from learning import models, serializer
import json
from django.core import serializers
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
import knox
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from knox.auth import AuthToken, TokenAuthentication
from .serializer import Serializer_For_Register
from learning.serializer import FeedSerializer
from django.views import View
from rest_framework.decorators import action


# todo:
# posielanie fotky
# pridanie súboru k inzerátu, posielanie súborov
# vytvoriť swagger
# aktualizácia dokumentácie


@api_view(['POST'])
def login(request):
    login_ser = AuthTokenSerializer(data=request.data)
    login_ser.is_valid(raise_exception=True)
    user = login_ser.validated_data['user']
    _, token = AuthToken.objects.create(user)
    return Response({
        'prihlasovacie udaje': dict(username=user.username, email=user.email),
        'token': token
    })


@api_view(['POST'])
def register(request):
    register_ser = Serializer_For_Register(data=request.data)
    if register_ser.is_valid(raise_exception=True):
        user = register_ser.save()
        _, token = AuthToken.objects.create(user)
        return Response({
            "registrovane udaje": dict(username=user.username, email=user.email),
            "token": token
        })


'''
@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request,username=email,password=password)
        if user is not None:
            return HttpResponse(status=200)
        else:
            return HttpResponse('Zle udaje', status=401)

'''

'''
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
            return HttpResponse('Already used email ' + data['email'], status=405)
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
        user = models.Users(name=data['name'],
                            surname=data['surname'],
                            email=data['email'],
                            password=data['password'],
                            photo=img_name + img_extension,
                            created_at=timezone.now(),
                            updated_at=timezone.now())
        user.save()
        user = User.objects.create_user('john', 'dk@dk', 'dkdk')
        token = Token.objects.create(user=user)
        return HttpResponse(token, status=200)
'''


class MyView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request,format=None):
        return HttpResponseNotFound("Inzerat s tymto id neexistuje")


@csrf_exempt
def inzeraty_id(request, inzerat_id):
    if request.method == 'GET':
        if models.Files.objects.filter(feed=inzerat_id) is not None:
            files = models.Files.objects.filter(feed=inzerat_id)
            file_name = []
            for item in files:
                file_name.append(item.file_name)
        try:
            model = models.Feed.objects.filter(pk=inzerat_id)
            data = serializers.serialize("json", model)
            return HttpResponse([file_name, data], status=200)
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


def get_file(request, inzerat_id):
    if request == 'GET':
        if models.Files.objects.filter(feed=inzerat_id) is not None:
            files = models.Files.objects.filter(feed=inzerat_id)
            file_arr = []
            for item in files:
                with open('learning/files/{0}'.format(item.file_name), "rb") as f:
                    file = f.read()
                    file_type = os.path.splitext('321bc5cc-7ac4-450a-af5d-1263dc4cedc9.jpg')[1]
                    file_arr.append([file, file_type])
            HttpResponse(file_arr, status=200)
    return HttpResponse(status=404)


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
            data = serializers.serialize('json', User.objects.filter(pk=user_id).values_list('email', ))
            return HttpResponse(data, status=200)
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
    print(request.user)
    if request.user.is_authenticated:
        print('je prihlaseny')
    if request.method == 'GET':
        data = serializers.serialize('json', models.Feed.objects.all())
        return HttpResponse(data, status=200)
    if request.method == 'POST':
        data = json.loads(request.POST['content'])
        model = models.Feed(title=data['title'],
                            description=data['description'],
                            created_at=timezone.now(),
                            updated_at=timezone.now(),
                            user=models.Users.objects.first())
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
                models.Files(file_name=name + extension,
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
