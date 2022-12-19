from django.test import TestCase

from invoice.forms.forms import OwnerForm
from invoice.models import OwnerModel


class OwnerFormTest(TestCase):

	def test_form(self):
		form = OwnerForm(data={
			'name': "Test"
		})
		self.assertFalse(form.is_valid())