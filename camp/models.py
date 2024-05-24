from django.db import models
from utils.iban_calculator import IBANCalculator


class SummerCampInfo(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    price = models.IntegerField()

    advisor_name = models.CharField(max_length=255, blank=True)
    advisor_id_number = models.CharField(max_length=255, blank=True)
    advisor_address = models.CharField(max_length=255, blank=True)

    main_manager = models.CharField(max_length=255, blank=True)
    main_manager_phone = models.CharField(max_length=255, blank=True)
    main_manager_email = models.EmailField(max_length=255, blank=True)

    chef_name = models.CharField(max_length=255, blank=True)
    chef_phone = models.CharField(max_length=255, blank=True)
    chef_email = models.EmailField(max_length=255, blank=True)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Check if an instance already exists
        existing_instance = SummerCampInfo.objects.first()

        if existing_instance:
            # If an instance exists, update its fields
            SummerCampInfo.objects.filter(id=existing_instance.id).update(
                name = self.name,
                start_date = self.start_date,
                end_date = self.end_date,
                price = self.price,
                advisor_name = self.advisor_name,
                advisor_id_number = self.advisor_id_number,
                advisor_address = self.advisor_address,
                main_manager = self.main_manager,
                main_manager_phone = self.main_manager_phone,
                main_manager_email = self.main_manager_email,
                chef_name = self.chef_name,
                chef_phone = self.chef_phone,
                chef_email = self.chef_email
            )
        else:
            # If no instance exists, create a new one
            super().save(*args, **kwargs)

        try:
            for ministrant in models.Ministrant.objects.all():
                ministrant.qr_pay_code = None
                ministrant.save()
        except AttributeError:
            pass

    class Meta:
        verbose_name = "Camp Information"
        verbose_name_plural = "Camp Information"

class BankAccount(models.Model):
    name = models.CharField(max_length=100)
    prefix_account_number = models.IntegerField()
    account_number = models.IntegerField()
    bank_code = models.CharField(max_length=100)
    variable_symbol_prefix = models.IntegerField()
    iban = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        # Check if an instance already exists
        existing_instance = BankAccount.objects.first()
        iban_calculator = IBANCalculator('CZ', self.account_number, self.bank_code, self.prefix_account_number)
        self.iban = iban_calculator.make_iban()

        if existing_instance:
            # If an instance exists, update its fields
            BankAccount.objects.filter(id=existing_instance.id).update(
                name=self.name,
                prefix_account_number=self.prefix_account_number,
                account_number=self.account_number,
                bank_code=self.bank_code,
                variable_symbol_prefix=self.variable_symbol_prefix,
                iban=self.iban
            )
        else:
            # If no instance exists, create a new one
            super().save(*args, **kwargs)

        try:
            for ministrant in models.Ministrant.objects.all():
                ministrant.qr_pay_code = None
                ministrant.save()
        except AttributeError:
            pass

        return None

    class Meta:
        verbose_name = "Bank Account"
        verbose_name_plural = "Bank Account"



