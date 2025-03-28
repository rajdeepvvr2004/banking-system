from django.db import models
from decimal import Decimal


class BankAccount(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    balance = models.IntegerField(null=False)
    email = models.EmailField(max_length=100)
    accountno = models.CharField(max_length=12)
    account_type=models.CharField(max_length=20,default="Savings")

    def __str__(self):
        return self.username


class Transaction(models.Model):
    user = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True) 
    type = models.CharField(max_length=10)  # 'Deposit' or 'Withdraw'
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.type} - Rs{self.amount}"  


class SavingsAccount(models.Model):
    account = models.OneToOneField(BankAccount, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)  # Keeping username here
    minimum_balance = models.DecimalField(max_digits=12, decimal_places=2, default=500.00)

    def __str__(self):
        return f"Savings Account - {self.username}"


class CurrentAccount(models.Model):
    account = models.OneToOneField(BankAccount, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)  # Keeping username here
    minimum_balance = models.DecimalField(max_digits=12, decimal_places=2, default=1000.00)

    def __str__(self):
        return f"Current Account - {self.username}"


class FixedDepositAccount(models.Model):
    account = models.OneToOneField(BankAccount, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)  # Keeping username here
    deposit_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=7.0)  # 7% interest
    duration_in_years = models.IntegerField()  # How many years the deposit is for
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fixed Deposit - {self.username}"

    def calculate_interest(self):
        """Calculates total interest earned for the duration."""
        interest = self.deposit_amount * (self.interest_rate / 100) * self.duration_in_years
        return interest
