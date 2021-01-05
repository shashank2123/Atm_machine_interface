from django.db import models

# Create your models here.
class gender(models.Model):
    gender_type=models.CharField(max_length=20)


class customer(models.Model):
    customerID=models.CharField(max_length=10,primary_key=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=30)
    address=models.TextField()
    dob=models.DateField()
    email=models.CharField(max_length=50)
    Phone_num=models.CharField(max_length=10)
    img=models.ImageField(upload_to='profile')
    gender=models.ForeignKey(to=gender,on_delete=models.DO_NOTHING)

class Account_status(models.Model):
    idStatus=models.AutoField(primary_key=True)
    status=models.CharField(max_length=20)

class Accounts(models.Model):
    idAccount=models.AutoField(primary_key=True)
    activated_date=models.DateField()
    status=models.ForeignKey(to=Account_status,on_delete=models.DO_NOTHING)
    last_access=models.DateTimeField(auto_now_add=True)
    balance=models.FloatField(null=False,)
    hold_on=models.ManyToManyField(to=customer)

class cardType(models.Model):
    idType=models.AutoField(primary_key=True)
    type=models.CharField(max_length=20)

class cardDetails(models.Model):
    numCard=models.CharField(max_length=12,primary_key=True)
    idAccount=models.ForeignKey(to=Accounts,on_delete=models.CASCADE)
    numType=models.ForeignKey(to=cardType,on_delete=models.DO_NOTHING)
    expire_year=models.IntegerField()
    expire_month=models.IntegerField()
    max_amount=models.FloatField()
    pin=models.CharField(max_length=4)

class transcations(models.Model):
    id=models.AutoField(primary_key=True)
    account_id=models.ForeignKey(to=Accounts,on_delete=models.DO_NOTHING)
    description=models.CharField(max_length=60)
    tran_time=models.DateTimeField(auto_now_add=True)
    balance=models.FloatField()

class loan(models.Model):
    accound_id=models.OneToOneField(to=Accounts,on_delete=models.CASCADE,primary_key=True)
    ammount=models.FloatField()
