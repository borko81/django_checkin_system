from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve

from invoice.views import (
	ShowAllInvoices, show_invoice,
	generate_fac, main_page_for_invoice, generate_and_edit_owner,
	ContractView, ConctractNew, ContractEdit
)


class TestInvoicesURL(TestCase):

	def test_show_all_invoices(self):
		url = reverse('show_all_invoices')
		self.assertEqual(resolve(url).func.view_class, ShowAllInvoices)

	def test_show_one_invoice(self):
		url = reverse('show_invoice', args=[1])
		self.assertEqual(resolve(url).func, show_invoice)

	def test_generate_new(self):
		url = reverse('generate_new')
		self.assertEqual(resolve(url).func, generate_fac)

	def test_invoice_menu(self):
		url = reverse('invoice_menu')
		self.assertEqual(resolve(url).func, main_page_for_invoice)


class TestOwnerAndContractUrls(TestCase):

	def test_owner_url(self):
		url = reverse('owner')
		self.assertEqual(resolve(url).func, generate_and_edit_owner)

	def test_show_contracts_urls(self):
		url = reverse('contracts')
		self.assertEqual(resolve(url).func.view_class, ContractView)

	def test_create_new_contract_url(self):
		url = reverse('contract_new')
		self.assertEqual(resolve(url).func.view_class, ConctractNew)

	def test_edit_contract_data_url(self):
		url = reverse('contract_edit', args=[1])
		self.assertEqual(resolve(url).func.view_class, ContractEdit)