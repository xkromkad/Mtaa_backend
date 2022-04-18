import os
import uuid
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from . import models
import json
from django.core import serializers
from django.utils import timezone
import base64


def authenticate(request, model):
    if 'token' in request.headers:
        user = models.token.objects.filter(token=request.headers['token']).first()
        if user is not None:
            if user.user_id == model:
                return True
    return False



@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if 'email' and 'password' not in data:
            return HttpResponse(status=401)
        model = models.Users.objects.filter(email=data['email'], password=data['password']).first()
        if model is not None:
            tok = models.token.objects.filter(user=model).first()
            if tok is not None:
                id = tok.token
            else:
                id = str(uuid.uuid4())
                models.token(token=id,
                             user=model).save()
            response = HttpResponse(status=200)
            response["token"] = id
            return response
        return HttpResponse(status=401)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)['req']
        email = models.Users.objects.filter(email=data['email']).first()
        if email is not None and data['email'] == email.email:
            return HttpResponse('Already used email '+data['email'], status=405)
    if request.FILES.get("image", None) is not None:
        img = request.FILES["image"]
        img_extension = os.path.splitext(img.name)[1]
        save_path = "learning/images"
        img_name = str(uuid.uuid4())
        img_save_path = "%s/%s%s" % (save_path, img_name, img_extension)
        with open(img_save_path, "wb+") as f:
            for chunk in img.chunks():
                f.write(chunk)
        image = img_name + img_extension
    else:
        image = 'None.png'
    model = models.Users(name = data['name'],
                 surname = data['surname'],
                 email = data['email'],
                 password = data['password'],
                 photo = image,
                 created_at = timezone.now(),
                 updated_at = timezone.now())
    model.save()
    id = str(uuid.uuid4())
    models.token(token=id,
                 user=model).save()
    response = HttpResponse(status=200)
    response["token"] = id
    return response

@csrf_exempt
def inzeraty_id(request, inzerat_id):
    if request.method == 'GET':
        if models.Files.objects.filter(feed=inzerat_id) is not None:
            files = models.Files.objects.filter(feed=inzerat_id)
            file_name = []
            for item in files:
                file_name.append(item.file_name)
            file_arr = json.dumps({"file_arr": file_name})
        else:
            file_arr = None
        try:
            model = models.Feed.objects.select_related('user').filter(pk=inzerat_id)
            print(model[0].title)
            data = json.dumps({"id": model[0].id, "title": model[0].title, "description": model[0].description,
                    "user_id": model[0].user_id, "name": model[0].user.name, "surname": model[0].user.surname})
            response = json.dumps({"data": data, "file_arr": file_arr})
            return HttpResponse(response, status=200)
        except models.Feed.DoesNotExist:
            return HttpResponseNotFound("Inzerat s tymto id neexistuje")
    if request.method == 'DELETE':
        model = models.Feed.objects.filter(pk=inzerat_id).first()
        if authenticate(request, model.user_id) is False:
            return HttpResponse(status=401)
        try:
            files = models.Files.objects.filter(feed=model)
            if files is not None:
                for file in files:
                    os.remove("learning/files/{0}".format(file.file_name))
                    file.delete()
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
        model.delete()
        return HttpResponse(status=204)
    if request.method == 'PUT':
        model = models.Feed.objects.filter(pk=inzerat_id).first()
        if authenticate(request, model.user_id) is False:
            print(model.user_id)
            return HttpResponse(status=401)
        data = json.loads(request.body)
        if 'title' in data:
            model.title = data['title']
        if 'description' in data:
            model.description = data['description']
        model.save()
        return HttpResponse(status=200)

@csrf_exempt
def users_id(request, user_id):
    if request.method == 'GET':
        try:
            print('tu')
            userik = models.Users.objects.get(email=user_id)
            item = userik.photo
            with open('learning/images/{0}'.format(item), "rb") as f:
                file = f.read()
                file = base64.b64encode(file).decode('utf-8')
            values = {"name": userik.name, "surname": userik.surname,
                      "email": userik.email, "photo": userik.photo, "file": file}
            print(file)
            return HttpResponse(json.dumps(values), status=200)
        except models.Users.DoesNotExist:
            return HttpResponseNotFound("Pouzivatel s tymto id neexistuje")
    if request.method == 'PUT':
        model = models.Users.objects.filter(pk=user_id).first()
        if authenticate(request, model.id) is False:
            return HttpResponse(status=401)
        data = json.loads(request.body)
        if 'name' in data:
            model.name = data['name']
        if 'surname' in data:
            model.surname = data['surname']
        if 'email' in data:
            model.email = data['email']
        if 'password' in data:
            model.password = data['password']
        model.save()
        return HttpResponse(status=200)
    if request.method == 'DELETE':
        model = models.Users.objects.filter(pk=user_id).first()
        if authenticate(request, model.id) is False:
            return HttpResponse(status=401)
        model.delete()
        return HttpResponse(status=204)


@csrf_exempt
def inzeraty(request):
    if request.method == 'GET':
        data = models.Feed.objects.raw(
            'SELECT "Feed".id, "Users".id as uid, title, description, name, surname FROM "Feed" JOIN "Users" ON '
            'user_id="Users".id')
        response = []
        for item in data:
            response.append({"name": item.name, "surname": item.surname, "title": item.title,
                             "description": item.description, "id": item.id, "uid": item.uid})
        response = json.dumps(response)
        return HttpResponse(response, status=200)
    if request.method == 'POST':
        if 'token' in request.headers:
            tk = models.token.objects.filter(token=request.headers['token']).first()
            if tk is None:
                return HttpResponse(status=401)
        else:
            return HttpResponse(status=401)
        user = models.Users.objects.filter(pk=tk.user_id).first()
        model = models.Feed(title = request.POST['title'],
                    description = request.POST['description'],
                    created_at = timezone.now(),
                    updated_at = timezone.now(),
                    user = user)
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


def get_file(request, inzerat_id):
    if request.method == 'GET':
        if models.Files.objects.filter(feed=inzerat_id) is not None:
            files = models.Files.objects.filter(feed=inzerat_id)
            file_arr = []
            for item in files:
                with open('learning/files/{0}'.format(item.file_name), "rb") as f:
                    file = f.read()
                    file_type = os.path.splitext(item.file_name)[1]
                    file_arr.append([file, file_type])
            print(base64.b64encode(file))
            file = base64.b64encode(file).decode('utf-8')
            js = json.dumps({"file": file})
            return HttpResponse(js, status=200)
    return HttpResponse(status=404)

