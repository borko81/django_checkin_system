from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve

from mpass.group_views import groups, new_group, group_edit, group_delete
from mpass.staff_views import persons, new_person, person_detail, delete_person
from mpass.cards_views import (
    show_all_cards, create_new_card,
    show_custom_card, delete_card, edit_card
)

from mpass.action_view import show_in_out

from mpass.emotial_view import (
    show_all_in_house, passage,
    total_time_in_house
)

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


class TestCardUrls(TestCase):
    def test_url_show_all_cards(self):
        url = reverse('show_all_cards')
        self.assertEqual(resolve(url).func, show_all_cards)

    def test_url_create_new_card(self):
        url = reverse('create_new_card')
        self.assertEqual(resolve(url).func, create_new_card)

    def test_url_show_custom_card(self):
        url = reverse('show_custom_card', args=[1])
        self.assertEqual(resolve(url).func, show_custom_card)

    def test_url_delete_card(self):
        url = reverse('delete_card', args=[1])
        self.assertEqual(resolve(url).func, delete_card)

    def test_url_for_edit_card(self):
        url = reverse('edit_card', args=[1])
        self.assertEqual(resolve(url).func, edit_card)


class TestActionUrls(TestCase):
    def test_url_for_show_in_out(self):
        url = reverse('show_in_out')
        self.assertEqual(resolve(url).func, show_in_out)


class TestEmotialUrls(TestCase):

    def setUp(self):
        self.client = Client()

    def test_url_inhouse(self):
        url = reverse('inhouse')
        self.assertEqual(resolve(url).func, show_all_in_house)

    def test_url_for_passage(self):
        url = reverse('passage')
        self.assertEqual(resolve(url).func, passage)

    def test_url_for_total_time(self):
        url = reverse('total_time')
        response = self.client.get(url)
        self.assertEqual(resolve(url).func, total_time_in_house)