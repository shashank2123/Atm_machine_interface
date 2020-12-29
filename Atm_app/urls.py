from django.urls import path
from . import views

urlpatterns =[
    path(r'',views.index,name='index'),
    path(r'insert',views.insert,name='insert'),
    path(r'pin',views.pin,name='insert'),
    path(r'check_balance',views.check_balance,name='check_balance')
]
