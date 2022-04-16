from django.urls import path
from . import views

urlpatterns = [
    path('prihlasenie', views.login, name='prihlasenie'),
    path('registracia', views.register, name='registracia'),
    path('inzeraty/<inzerat_id>', views.inzeraty_id, name='inzeraty_id'),
    path('pouzivatelia/<user_id>', views.users_id, name='users_id'),
    path('inzeraty', views.inzeraty, name='list'),
    # path('/pouzivatel/inzeraty/<inzerat-id>', views.feed_edit, name = 'feed_edit')

]