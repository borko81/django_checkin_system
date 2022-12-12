from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve

from mpass.group_views import groups, new_group, group_edit, group_delete
from mpass.staff_views import persons, new_person, person_detail, delete_person


class TestGroupUrls(TestCase):
    def test_all_groups_url(self):
        url = reverse("groups")
        self.assertEqual(resolve(url).func, groups)

    def test_add_group(self):
        url = reverse("new_group")
        self.assertEqual(resolve(url).func, new_group)

    def test_group_edit(self):
        url = reverse("group_edit", args=[1])
        self.assertEqual(resolve(url).func, group_edit)
        url2 = reverse("group_edit", args=[1, "new name"])
        self.assertEqual(resolve(url2).func, group_edit)

    def test_group_delete(self):
        url = reverse("group_delete", args=[1])
        self.assertEqual(resolve(url).func, group_delete)


class TestPersonUrls(TestCase):
    def test_url_show_all_persons(self):
        url = reverse("persons")
        self.assertEqual(resolve(url).func, persons)

    def test_url_for_create_new_person(self):
        url = reverse("new_person")
        self.assertEqual(resolve(url).func, new_person)

    def test_url_person_detail(self):
        url = reverse("person_detail", args=[1])
        self.assertEqual(resolve(url).func, person_detail)

    def test_url_person_delete(self):
        url = reverse("delete_person", args=[1])
        self.assertEqual(resolve(url).func, delete_person)
