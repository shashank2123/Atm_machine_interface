from django.shortcuts import render,redirect
from .models import cardDetails,Accounts
from django.contrib import messages

# Create your views here.
def index(request):
    return(render(request,'insert_card.html'))

def insert(request):
    if request.method=="POST":
        num=request.POST['cardnum']
        request.session['num']=num
        if cardDetails.objects.filter(numCard=num).exists():
            return(render(request,'pin.html'))
        else:
            messages.warning(request,"Invalid card number")
            return(render(request,'insert_card.html'))
    else:
        return(render(request,'insert_card.html'))
def pin(request):
    if request.method=='POST':
        num=request.session.get('num')
        pin=request.POST["pass"]
        original_pin=cardDetails.objects.all().filter(numCard=num).values_list('pin',flat=True)[0]
        if pin==original_pin:
            return(render(request,'options.html'))
        else:
            messages.warning(request,"Invalid pin")
            return(render(request,'pin.html'))
    else:
        return(render(request,'pin.html'))
def check_balance(request):
    num=request.session.get('num')
    account_num=cardDetails.objects.all().filter(numCard=num).values_list('idAccount',flat=True)[0]
    account_balance=Accounts.objects.all().filter(pk=account_num).values_list('balance',flat=True)[0]
    return(render(request,'checkbl.html',{'account_balance':account_balance}))
