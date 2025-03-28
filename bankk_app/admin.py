# Register your models here.
from django.contrib import admin
from .models import BankAccount,Transaction,SavingsAccount,CurrentAccount,FixedDepositAccount

admin.site.register(BankAccount)

admin.site.register(Transaction)

admin.site.register(SavingsAccount)

admin.site.register(CurrentAccount)

admin.site.register(FixedDepositAccount)


