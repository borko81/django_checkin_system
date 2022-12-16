from django.test import TestCase
from django.db.utils import IntegrityError

from ...models import GroupModel, PersonInformationModel, CardsModel, ActionModel


class GroupModelTests(TestCase):
    def setUp(self):
        group = GroupModel.objects.create(name="First Group")

    def test_group_is_successfully_created(self):
        g = GroupModel.objects.get(id=1)
        self.assertEqual(g.name, "First Group")

    def test_create_group_name_be_not_unique_should_raise_error(self):
        with self.assertRaises(IntegrityError):
            GroupModel.objects.create(name="First Group")


class PersonModelTests(TestCase):
    def setUp(self) -> None:
        group = GroupModel.objects.create(name="First Group")
        user = PersonInformationModel.objects.create(
            name="Some Name", group=group, tel="0888112233"
        )

    def test_corect_data_from_record(self):
        data = PersonInformationModel.objects.get(id=1)
        self.assertEqual(data.name, "Some Name")
        self.assertEqual(data.group.name, "First Group")

    def test_valid_data_to_dict(self):
        data = PersonInformationModel.objects.get(id=1)
        data_to_dict = data.to_dict()
        self.assertEqual(data_to_dict["name"], "Some Name")


class CardModelTests(TestCase):
    def setUp(self):
        n = 10
        for i in range(n):
            CardsModel.objects.create(card=str(i).zfill(12))

    def test_all_card_is_created(self):
        self.assertEqual(len(CardsModel.objects.all()), 10)
        self.assertEqual(all(i.is_valid for i in CardsModel.objects.all()), True)

    def test_assign_card_to_person(self):
        group = GroupModel.objects.create(name="1First Group")
        check_user = PersonInformationModel.objects.create(
            name="Some Name", group=group, tel="0888112233"
        )
        first_card = CardsModel.objects.get(id=1)
        first_card.person_id = check_user

        self.assertEqual(first_card.person_id.name, "Some Name")

    def test_model_to_dict(self):
        group = GroupModel.objects.create(name="1First Group")
        check_user = PersonInformationModel.objects.create(
            name="Some Name", group=group, tel="0888112233"
        )
        first_card = CardsModel.objects.get(id=1)
        first_card.person_id = check_user

        actual_result = {
            "id": 1,
            "name": "000000000000",
            "is_valid": True,
            "person_id": 1,
            "from": None,
            "to": None
        }

        self.assertEqual(first_card.to_dict(), actual_result)

    def test_clear_valid_from_and_to_when_save_without_person(self):
        new_card_for_test = CardsModel(
            card="123A321",
            valid_from="2022-12-15",
            valid_to="2022-12-25"
        )

        new_card_for_test.save()
        self.assertEqual(new_card_for_test.valid_to, None)