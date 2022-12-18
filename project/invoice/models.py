from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from decimal import Decimal


FAK_TYPE = (("1", "Фактура"), ("2", "Проформа"), ("3", "Кредитно известие"))


PAY_TYPE = (("1", "Брой"), ("2", "Банка"), ("3", "Кредитна карта"), ("4", "Ваучер"))


class FirmData(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=120, blank=False, null=False)
    town = models.CharField(max_length=100, null=False, blank=False)
    address = models.CharField(max_length=120, blank=False, null=False)
    mol = models.CharField(max_length=120, blank=False, null=False)
    bulstat = models.CharField(max_length=13, blank=False, null=False)
    idmum = models.CharField(max_length=15, blank=True, null=True)


class OwnerModel(FirmData, models.Model):
    class Meta:
        db_table = "owner"

    email = models.EmailField(max_length=254, blank=True, null=True)
    tel = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class OwnerNumbers(models.Model):
    class Meta:
        db_table = "last_fak_number"

    last_fak_id = models.CharField(max_length=10)
    last_proform_id = models.CharField(max_length=10)
    owner_id = models.ForeignKey(
        OwnerModel, on_delete=models.CASCADE, blank=False, null=False
    )

    # def save(self, *args, **kwargs):
    #     """ Only one row in that table allowed """
    #     if self.__class__.objects.count():
    #         self.pk = self.__class__.objects.first().pk
    #     else:    
    #         self.last_fak_id = str(self.last_fak_id).zfill(10)
    #         self.ast_proform_id = str(self.last_proform_id).zfill(10)
    #         super().save(*args, **kwargs)

    def __str__(self):
        return self.last_fak_id


class Contragent(FirmData, models.Model):
    class Meta:
        db_table = "contragents"

    from_who = models.CharField(max_length=120, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class BankAcc(models.Model):
    class Meta:
        db_table = "bank"

    banc_name = models.CharField(max_length=32)
    bank_acc_kod = models.CharField(max_length=8)
    bank_acc_smetka = models.CharField(max_length=30)
    owner_id = models.ForeignKey(
        OwnerModel, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return self.banc_name


class FakId(models.Model):
    class Meta:
        db_table = "fak"

    number = models.CharField(max_length=10)
    tip = models.CharField(max_length=1, choices=FAK_TYPE, default=1)
    pay_type = models.CharField(max_length=1, choices=PAY_TYPE, default=1)

    neto = models.DecimalField(max_digits=10, decimal_places=2)
    dds = models.IntegerField()
    dds_suma = models.DecimalField(max_digits=10, decimal_places=2)
    fak_total = models.DecimalField(max_digits=10, decimal_places=2)

    contract_id = models.ForeignKey(
        Contragent, on_delete=models.CASCADE, null=True, blank=True
    )
    data_sdelka = models.DateField(auto_now_add=True)
    data_padej = models.DateField(blank=True, null=True)

    # pari_basis = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(fak_total) - Decimal(dds_suma))

    def save(self, *args, **kwargs):
        o = OwnerNumbers.objects.first()
        if not self.number:
            self.number = str(int(o.last_fak_id) + 1).zfill(10)
            o.last_fak_id = self.number
            o.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.number


class FakElelements(models.Model):
    class Meta:
        db_table = "fak_elements"

    faktura_id = models.ForeignKey(
        FakId,
        related_name="faktura_id",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    text = models.CharField(max_length=120)
    kol = models.IntegerField()
    brutna_cena = models.DecimalField(max_digits=10, decimal_places=2)
    dds = models.IntegerField()


    element_suma = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    dds_suma = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    element_total = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        self.element_suma = round(
            (self.brutna_cena * self.kol) / Decimal(1 + self.dds / 100), 2
        )
        self.dds_suma = self.brutna_cena * self.kol - self.element_suma
        self.element_total = self.element_suma / self.kol
        super().save(*args, **kwargs)


@receiver(post_save, sender=FakElelements)
def create_fak_after_elements(sender, instance, **kwargs):
    neto = instance.element_suma
    dds = instance.dds
    dds_suma = instance.dds_suma
    fak_total = instance.brutna_cena * instance.kol
    contract = Contragent.objects.get(id=2)

    if not instance.faktura_id:
        o = OwnerNumbers.objects.first()

        f = FakId(
            neto=neto,
            dds=dds,
            dds_suma=dds_suma,
            fak_total=fak_total,
            number = str(int(o.last_fak_id) + 1).zfill(10)
        )
        # import pdb;pdb.set_trace()
        o.last_fak_id = f.number
        o.save()
        f.save()

        instance.faktura_id = f
        instance.save()

    else:
        fak_target = FakId.objects.get(id=instance.faktura_id.id)
        # import pdb;pdb.set_trace()
        fak_target.neto = neto
        fak_target.dds = dds
        fak_target.dds_suma = dds_suma
        fak_target.fak_total = fak_total
        # fak_target.contract_id = Contragent.objects.all()[0]
        fak_target.save()
