from django.urls import path

from .views import show_invoice, generate_fac

urlpatterns = [ 
	path('show/<int:id_>', show_invoice, name='show_invoice'),
	path('generate_new/', generate_fac, name='generate_new'),
]