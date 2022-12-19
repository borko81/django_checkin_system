from django.urls import path

from .views import (
	show_invoice, generate_fac, generate_and_edit_owner,
	main_page_for_invoice, ContractView, ConctractNew, ContractEdit, ShowAllInvoices
)

urlpatterns = [ 
	path('show/', ShowAllInvoices.as_view(), name='show_all_invoices'),
	path('show/<int:id_>', show_invoice, name='show_invoice'),
	path('generate_new/', generate_fac, name='generate_new'),
	path('', main_page_for_invoice, name='invoice_menu'),
	path('owner/', generate_and_edit_owner, name='owner'),
	path('contracts/', ContractView.as_view(), name='contracts'),
	path('contract/new/', ConctractNew.as_view(), name='contract_new'),
	path('contract/edit/<int:pk>/', ContractEdit.as_view(), name='contract_edit'),
]