from django.urls import path
from . import views

urlpatterns = [
    path('prihlasenie', views.login, name='prihlasenie'),
    path('registracia', views.register, name='registracia'),
    path('inzeraty/<inzerat_id>', views.inzeraty_id, name='inzeraty_id'),
    path('inzeraty/vsetky', views.inzeraty_all, name='inzeraty_all'),
    path('pouzivatelia/<user_id>', views.users_id, name='users_id'),
    path('inzeraty', views.list, name='list'),
    # path('registracia', views.register, name='registracia'),

]