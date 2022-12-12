from django.contrib import admin

from .models import *


@admin.register(GroupModel)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(PersonInformationModel)
class PersonInfoAdmin(admin.ModelAdmin):
    list_display = "name group".split()


@admin.register(CardsModel)
class CardAdmin(admin.ModelAdmin):
    pass


@admin.register(ActionModel)
class ActionAdmin(admin.ModelAdmin):
    pass


@admin.register(OnlyInHouse)
class OnlyInHouseAdmin(admin.ModelAdmin):
    pass
