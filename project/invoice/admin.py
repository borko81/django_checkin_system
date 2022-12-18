from django.contrib import admin

from .models import OwnerModel, OwnerNumbers, BankAcc, Contragent, FakId, FakElelements


@admin.register(OwnerModel)
class OwnerModelAdmin(admin.ModelAdmin):
    list_display = "name bulstat".split()


@admin.register(OwnerNumbers)
class OwnerNumbersAdmin(admin.ModelAdmin):
    pass


@admin.register(BankAcc)
class BankAccAdmin(admin.ModelAdmin):
    pass


@admin.register(Contragent)
class ContragentAdmin(admin.ModelAdmin):
    list_display = "name bulstat is_active".split()


@admin.register(FakId)
class FakIdAdmin(admin.ModelAdmin):
    list_display = "number tip pay_type fak_total contract_id data_sdelka".split()


@admin.register(FakElelements)
class FakElelements(admin.ModelAdmin):
    pass
