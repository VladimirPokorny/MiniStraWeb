from django.db import models
from utils.iban_calculator import IBANCalculator


class SummerCampInfo(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    price = models.IntegerField()

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Check if an instance already exists
        existing_instance = SummerCampInfo.objects.first()

        if existing_instance:
            # If an instance exists, update its fields
            existing_instance.name = self.name
            existing_instance.start_date = self.start_date
            existing_instance.end_date = self.end_date
            existing_instance.price = self.price
            existing_instance.save()
        else:
            # If no instance exists, create a new one
            super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Camp Information"
        verbose_name_plural = "Camp Information"

class BankAccount(models.Model):
    name = models.CharField(max_length=100)
    account_number = models.IntegerField()
    bank_code = models.CharField(max_length=100)
    prefix_account_number = models.CharField(max_length=100)
    variable_symbol_prefix = models.IntegerField()
    iban = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs) -> None:
        # Check if an instance already exists
        existing_instance = BankAccount.objects.first()
        iban_calculator = IBANCalculator('CZ', self.account_number, self.bank_code, self.prefix_account_number)
        self.iban = iban_calculator.make_iban()

        if existing_instance:
            # If an instance exists, update its fields
            existing_instance.name = self.name
            existing_instance.number = self.number
            existing_instance.bank_code = self.bank_code
            existing_instance.variable_symbol_prefix = self.variable_symbol_prefix
            existing_instance.save()
        else:
            # If no instance exists, create a new one
            super().save(*args, **kwargs)
        
        return None

    class Meta:
        verbose_name = "Bank Account"
        verbose_name_plural = "Bank Account"



