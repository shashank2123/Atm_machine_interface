from django.shortcuts import render,redirect,HttpResponse
from .models import cardDetails,Accounts,cardType,transcations,loan,customer,pin
from django.contrib import messages
from django.db import connection
import plotly.express as px
import numpy as np
from Atm_min_project.settings import STATIC_DIR
import os
from datetime import datetime,timedelta
import io
import PIL.Image as Image
# Create your views here.
def welcome(request):
    return(render(request,'Welcome.html'))
def index(request):
    return(render(request,'insert_card.html'))

def insert(request):
    if request.method=="POST":
        num=request.POST['cardnum']
        request.session['num']=num
        if cardDetails.objects.filter(numCard=num).exists():
            card=cardDetails.objects.get(numCard=num)
            return(render(request,'pin.html'))
        else:
            messages.warning(request,"Invalid card number")
            return(render(request,'insert_card.html'))
    else:
        return(render(request,'insert_card.html'))

def options(request):
    return(render(request,'options.html'))

def pin_get(request):
    if request.method=='POST':
        num=request.session.get('num')
        pin=request.POST["pass"]
        old=cardDetails.objects.get(pk=num)
        original_pin=old.pin_id.code
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
    last_access=Accounts.objects.all().filter(pk=account_num).values_list('last_access',flat=True)[0]
    return(render(request,'checkbl.html',{'account_balance':account_balance,'last_access':last_access}))

def withdrawType(request):
    return(render(request,'withdraw.html'))

def withdrawAmmount(request):
    if request.method=='POST':
        num=request.session.get('num')
        type_id=cardDetails.objects.all().filter(numCard=num).values_list('numType_id',flat=True)[0]
        cardtype=cardType.objects.all().filter(pk=type_id).values_list('type',flat=True)[0]
        submit_type=request.POST['type']
        request.session['submit_type']=submit_type
        if submit_type=='debit' or cardtype==submit_type:
            return(render(request,'withamount.html'))
        elif cardtype=='debit' and submit_type=='credit':
            messages.warning(request,'Invalid Option')
            return(render(request,'withdraw.html'))
    else:
        return(render(request,'withdraw.html'))

def amount_with(request):
    if request.method=='POST':
        num=request.session.get('num')
        amount=float(request.POST['amount'])
        max_amount=cardDetails.objects.all().filter(numCard=num).values_list('max_amount',flat=True)[0]
        if amount<=max_amount:
            account_num=cardDetails.objects.all().filter(numCard=num).values_list('idAccount',flat=True)[0]
            account_balance=Accounts.objects.all().filter(pk=account_num).values_list('balance',flat=True)[0]
            account=Accounts.objects.get(pk=account_num)
            if request.session.get('submit_type')=='debit':
                if amount<=account_balance-250:
                    new_balance=account_balance-amount
                    Accounts.objects.all().filter(pk=account_num).update(balance=new_balance)
                    trans=transcations(account_id=account,description='debit',balance=new_balance,amount=amount)
                    trans.save()
                    return(render(request,'collectYourMoney.html'))
                else:
                    messages.warning(request,'Account balance is not sufficient')
                    return(render(request,'withamount.html'))
            else:
                try:
                    obj=loan(pk=account_num,ammount=amount)
                    obj.save()
                except:
                    obj=loan.objects.get(pk=account_num)
                    current_loan=obj.ammount
                    loan.objects.all().filter(pk=account_num).update(ammount=current_loan+float(amount))
                trans=transcations(account_id=account,description='credit',balance=account_balance,amount=amount)
                trans.save()
                return(render(request,'collectYourMoney.html'))
        else:
            messages.error(request,'limit exceded')
            return(render(request,'withamount.html'))
    else:
        return(render(request,'withamount.html'))


def  pinchange_redirect(request):
    num=request.session.get('num')
    last_pass_change=cardDetails.objects.all().filter(numCard=num).values_list('last_pinChange',flat=True)[0]
    return(render(request,'pchange.html',{'last_pass_change':last_pass_change}))

def pinchange(request):
    if request.method=='POST':
        new_pass=request.POST['new_pass']
        re_pass=request.POST['re_pass']
        if new_pass==re_pass:
            num=request.session.get('num')
            old=cardDetails.objects.get(pk=num)
            old_pass=old.pin_id.code
            if old_pass!=new_pass:
                pin.objects.all().filter(pk=old.pin_id.id).update(code=new_pass)
                return(render(request,'successful.html'))
            else:
                messages.error(request,'New PIN same as old PIN')
                return(render(request,'pchange.html'))
        else:
            messages.error(request,'password not matched')
            return(render(request,'pchange.html'))
    else:
        return(render(request,'pchange.html'))

def fastWithdrwa(request):
    return(render(request,'FastWithdraw.html'))

def fastAmount(request):
    if request.method=='POST':
        num=request.session.get('num')
        amount=float(request.POST['submit'])
        account_num=cardDetails.objects.all().filter(numCard=num).values_list('idAccount',flat=True)[0]
        account_balance=Accounts.objects.all().filter(pk=account_num).values_list('balance',flat=True)[0]
        if amount<=account_balance-250:
            account=Accounts.objects.get(pk=account_num)
            account_balance=account.balance
            new_balance=account_balance-amount
            Accounts.objects.all().filter(pk=account_num).update(balance=new_balance)
            trans=transcations(account_id=account,description='debit',balance=new_balance,amount=amount)
            trans.save()
            return(render(request,'collectYourMoney.html'))
        else:
            messages.warning(request,'Account balance is not sufficient')
            return(render(request,'FastWithdraw.html'))
    else:
        return(render(request,'FastWithdraw.html'))
def profileView(request):
    num=request.session.get('num')
    account_num=cardDetails.objects.all().filter(numCard=num).values_list('idAccount',flat=True)[0]
    account=Accounts.objects.get(pk=account_num)
    customers=account.hold_on.all()
    return(render(request,'profileView.html',context={'customers':customers}))
def profile(request):
    custNum=request.POST['cust']
    customerDetails=customer.objects.get(pk=custNum)
    return render(request,'profile.html',{'customer':customerDetails})

def my_custom_sql(num):
    with connection.cursor() as cursor:
        cursor.execute("CALL  SelectTransaction(%s)", [num])
        row = cursor.fetchall()
    return row

def history(request):
    num=request.session.get('num')
    account_num=cardDetails.objects.all().filter(numCard=num).values_list('idAccount',flat=True)[0]
    hist=tuple(reversed(my_custom_sql(account_num)))
    return(render(request,'history.html',{'hist':hist}))


def generate_report(request):
    query1="""SELECT id,account_id_id,SUM(amount) as amount
    FROM atm_app_transcations
    WHERE tran_time BETWEEN DATE_SUB(NOW(), INTERVAL 1 DAY) AND NOW()
    GROUP BY account_id_id"""
    transcations_data=transcations.objects.raw(query1)
    x=[]
    y=[]
    for obj in transcations_data:
        x.append(obj.account_id_id)
        y.append(obj.amount)
    x=np.array(x)
    y=np.array(y)
    high=y.argmax()
    low=y.argmin()
    high_time=datetime.now()
    low_time=high_time-timedelta(days=1)
    high_time=high_time.strftime("%m/%d/%Y, %H:%M:%S")
    low_time=low_time.strftime("%m/%d/%Y, %H:%M:%S")
    text1="""In the peroid of {}-{}, Account ID {} has highest transaction amount and Account ID {}
            lowest transaction amount """.format(low_time,high_time,x[high],x[low])
    fig1 = px.bar(x=x, y = y ,labels=dict(x="Account ID", y="Amount"),text=y)
    fig1.update_xaxes(type='category')
    fig1.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig1.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig1.write_image(os.path.join(STATIC_DIR,"images","fig1.jpeg"))

    query2="""SELECT id,description,SUM(amount) as amount
    FROM atm_app_transcations
    WHERE tran_time BETWEEN DATE_SUB(NOW(), INTERVAL 1 DAY) AND NOW()
    GROUP BY description"""
    transcations_data=transcations.objects.raw(query2)
    x=[]
    y=[]
    for obj in transcations_data:
        x.append(obj.description)
        y.append(obj.amount)
    x=np.array(x)
    y=np.array(y)
    high_time=datetime.now()
    low_time=high_time-timedelta(days=1)
    high_time=high_time.strftime("%m/%d/%Y, %H:%M:%S")
    low_time=low_time.strftime("%m/%d/%Y, %H:%M:%S")
    text2="""In the peroid of {}-{},Total {} amount is {}
            and {} amount is {}. """.format(low_time,high_time,x[0],y[0],x[1],y[1])
    fig2 = px.bar(x=x, y = y ,labels=dict(x="Type", y="Amount"),text=y)
    fig2.update_xaxes(type='category')
    fig2.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig2.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig2.write_image(os.path.join(STATIC_DIR,"images","fig2.jpeg"))
    return render(request,'transactions_report.html',{'text1':text1,'text2':text2})
