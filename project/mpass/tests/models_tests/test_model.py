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
