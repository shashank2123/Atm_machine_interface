from django.urls import path
from . import views
app_name='Atm_app'

urlpatterns =[
    path(r'',views.welcome,name='home'),
    path(r'welcome',views.welcome,name='welcome'),
    path(r'index',views.index,name='index'),
    path(r'insert',views.insert,name='insert'),
    path(r'options',views.options,name='options'),
    path(r'pin',views.pin_get,name='pin'),
    path(r'check_balance',views.check_balance,name='check_balance'),
    path(r'withdraw',views.withdrawType,name='withdrawType'),
    path(r'withdrawAmmount',views.withdrawAmmount,name='withdrawAmmount'),
    path(r'pinredirect',views.pinchange_redirect,name='pinredirect'),
    path(r'pinchange',views.pinchange,name='pinchange'),
    path(r'amount_with',views.amount_with,name='amount_with'),
    path(r'fastWithdrwa',views.fastWithdrwa,name='fastWithdrwa'),
    path(r'fastAmount',views.fastAmount,name='fastAmount'),
    path(r'profileView',views.profileView,name='profileView'),
    path(r'profile',views.profile,name='profile'),
    path(r'history',views.history,name='history'),
    path(r'help',views.help,name='help'),

]
