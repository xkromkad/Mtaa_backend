from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

from learning import models
from .models import Feed


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def login(request):
    if request.method == 'POST':
        r = Feed.objects.get(pk=1)
        return HttpResponse(request.POST['name'])
    if request.method == 'DELETE':
        return HttpResponse('delete')


def register(request):
    return HttpResponse("Registracia")


def inzeraty_id(request, inzerat_id):
    try:
        inz = models.Feed.objects.get(pk=inzerat_id)
        inz = dict(inz.objects.values())
        return JsonResponse(inz, safe=False, status=200)
    except Feed.DoesNotExist:
        return HttpResponseNotFound("Inzerat s tymto id neexistuje")


def inzeraty_all(request):
   # inz = models.Feed.objects.get(pk=inzerat_id)
    # inz = dict(inz.objects.values())
    inzs = list(models.Feed.objects.values())
    return JsonResponse(inzs, safe=False, status=200)

def users_id(request, user_id):

    user = dict(models.Users.objects.values())
    return JsonResponse(user, safe=False, status=200)


