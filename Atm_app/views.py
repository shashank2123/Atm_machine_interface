from django.shortcuts import render,redirect
from .models import cardDetails,Accounts,cardType
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

def withdrawType(request):
    return(render(request,'withdraw.html'))

def withdrawAmmount(request):
    if request.method=='POST':
        num=request.session.get('num')
        type_id=cardDetails.objects.all().filter(numCard=num).values_list('numType_id',flat=True)[0]
        cardtype=cardType.objects.all().filter(pk=type_id).values_list('type',flat=True)[0]
        submit_type=request.POST['type']
        if submit_type=='debit' or cardtype==submit_type:
            return(render(request,'withamount.html'))
        elif cardtype=='debit' and submit_type=='credit':
            messages.warning(request,'Invalid Option')
            return(render(request,'withdraw.html'))
    else:
        return(render(request,'withdraw.html'))

def  pinchange_redirect(request):
    return(render(request,'pchange.html'))

def pinchange(request):
    if request.method=='POST':
        new_pass=request.POST['new_pass']
        re_pass=request.POST['re_pass']
        if new_pass==re_pass:
            num=request.session.get('num')
            old_pass=cardDetails.objects.all().filter(numCard=num).values_list('pin',flat=True)[0]
            if old_pass!=new_pass:
                cardDetails.objects.all().filter(numCard=num).update(pin=new_pass)
                return(render(request,'successful.html'))
            else:
                messages.error(request,'New PIN same as old PIN')
                return(render(request,'pchange.html'))
        else:
            messages.error(request,'password not matched')
            return(render(request,'pchange.html'))
    else:
        return(render(request,'pchange.html'))
