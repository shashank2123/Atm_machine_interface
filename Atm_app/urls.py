from django.urls import path
from . import views

urlpatterns =[
    path(r'',views.index,name='index'),
    path(r'insert',views.insert,name='insert'),
    path(r'pin',views.pin,name='insert'),
    path(r'check_balance',views.check_balance,name='check_balance'),
    path(r'withdraw',views.withdrawType,name='withdrawType'),
    path(r'withdrawAmmount',views.withdrawAmmount,name='withdrawType')
]
