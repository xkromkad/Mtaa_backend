from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Feed
from django.contrib.auth.models import User

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
    return HttpResponse(f"Inzerat {inzerat_id}")


def users_id(request, user_id):
    return HttpResponse(f"Pouzivatel {user_id}")


