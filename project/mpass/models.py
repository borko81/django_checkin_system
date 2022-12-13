from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class GroupModel(models.Model):
    objects = None
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class PersonInformationModel(models.Model):
    objects = None
    name = models.CharField(max_length=120)
    group = models.ForeignKey(
        GroupModel, on_delete=models.CASCADE, blank=False, null=False
    )
    tel = models.CharField(max_length=32, null=True, blank=True)
    picture = models.ImageField(upload_to="person_image", null=True, blank=True)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "name": self.name,
            "group": self.group.name,
            "tel": self.tel,
            "picture": self.picture,
        }


class CardManagerWithoutPerson(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()

    def without_person(self):
        return self.get_queryset().filter(person_id__isnull=True)

    def stoped_card(self):
        return self.get_queryset().filter(is_valid=False)

    def not_stoped_card(self):
        return self.get_queryset().filter(is_valid=True)


class CardsModel(models.Model):
    card = models.CharField(max_length=12, unique=True, null=False)
    is_valid = models.BooleanField(default=True)
    person_id = models.ForeignKey(
        PersonInformationModel, on_delete=models.CASCADE, blank=True, null=True
    )
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)

    # manager
    objects = models.Manager()
    custom_manager = CardManagerWithoutPerson()

    def __str__(self):
        return self.card

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.card,
            "is_valid": self.is_valid,
            "person_id": self.person_id.id,
            "from": self.valid_from,
            "to": self.valid_to,
        }

    def save(self, *args, **kwargs):
        if self.person_id is None or self.is_valid is False:
            self.valid_from = None
            self.valid_to = None
        super().save(*args, **kwargs)


@receiver(post_save, sender=CardsModel)
def update_valid_date(sender, instance, **kwargs):
    print(f"Save or edit card model: {instance}")


class ActionModel(models.Model):
    IN = "IN"
    OUT = "OUT"

    action_data = [(IN, "INCOME"), (OUT, "OUTCOME")]

    card_id = models.ForeignKey(CardsModel, on_delete=models.CASCADE)
    person_id = models.ForeignKey(PersonInformationModel, on_delete=models.CASCADE)
    action = models.CharField(max_length=3, choices=action_data, default=IN)
    data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.card_id.card


class OnlyInHouse(models.Model):
    card = models.ForeignKey(CardsModel, on_delete=models.CASCADE)
    when_come = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.card.card


@receiver(post_save, sender=ActionModel)
def only_in_house(sender, instance, **kwargs):
    action = instance.action
    card_id = instance.card_id
    when_come = instance.data_time

    if action == "IN":
        OnlyInHouse.objects.create(card=card_id, when_come=when_come)
    else:
        try:
            target = OnlyInHouse.objects.get(card=card_id)
            target.delete()
        except:
            pass
