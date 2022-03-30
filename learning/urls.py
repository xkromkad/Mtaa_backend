from django.urls import path
from rest_framework.routers import DefaultRouter
from django.urls.conf import include
from . import views
from learning.views import MyView

#router = DefaultRouter()
# router.register('inz', views.MyView)

urlpatterns = [
    path('prihlasenie', views.login, name='prihlasenie'),
    path('registracia', views.register, name='registracia'),
    path('inzeraty/<inzerat_id>', views.inzeraty_id, name='inzeraty_id'),
    path('pouzivatelia/<user_id>', views.users_id, name='users_id'),
    path('inzeraty', views.inzeraty_list, name='list'),
    path('inz', MyView.as_view(), name='INZ'),
    # path('', include(router.urls)),
    # path('/pouzivatel/inzeraty/<inzerat-id>', views.feed_edit, name = 'feed_edit')
    # path('inz/<inzerat_id>', MyView,name='inz'),
]