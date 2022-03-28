from django.urls import path
from . import views

urlpatterns = [
    path('prihlasenie', views.login, name='prihlasenie'),
    path('registracia', views.register, name='registracia'),
    path('inzeraty/<inzerat_id>', views.inzeraty_id, name='inzeraty_id'),
    path('pouzivatelia/<user_id>', views.users_id, name='users_id'),
    path('inzeraty', views.inzeraty_list, name='list'),
    # path('registracia', views.register, name='registracia'),
    # path('pouzivatel/<pouzivatel-id>/uprava ', views.user_settings, name = 'user_settings),
    # path('pouzivatel/<pouzivatel-id>', views.user, name = 'user'),
    # path('/pouzivatel/inzeraty/<inzerat-id>', views.feed_edit, name = 'feed_edit')

]