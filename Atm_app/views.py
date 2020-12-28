from django.shortcuts import render,redirect
from .models import cardDetails
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
        original_pin=cardDetails.objects.filter(numCard=num).values('pin')[0]['pin']
        if pin==original_pin:
            return(render(request,'options.html'))
        else:
            messages.warning(request,"Invalid pin")
            return(render(request,'pin.html'))
    else:
        return(render(request,'pin.html'))
