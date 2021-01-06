from django.contrib import admin
from .models import Accounts,Account_status,cardDetails,cardType,customer,gender,pin
# Register your models here.

admin.site.register(Accounts)
admin.site.register(Account_status)
admin.site.register(cardDetails)
admin.site.register(cardType)
admin.site.register(customer)
admin.site.register(gender)
admin.site.register(pin)
