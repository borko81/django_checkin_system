from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, CreateView, UpdateView

from .models import Contragent, OwnerNumbers, FakElelements, FakId, OwnerModel, BankAcc
from .forms import forms

from decimal import Decimal


def show_invoice(request, id_):
    owner = OwnerModel.objects.first()
    bank = BankAcc.objects.get(owner_id=owner.id)
    fak_id = FakId.objects.get(id=id_)
    fak_elementrs = FakElelements.objects.filter(faktura_id=fak_id.id)
    contract_id = Contragent.objects.get(id=fak_id.contract_id.id)
    context = {
        "title": "Show invoice",
        "id": fak_id,
        "bases": fak_id.fak_total - fak_id.dds_suma,
        "owner": owner,
        "bank": bank,
        "contract": contract_id,
        "elements": fak_elementrs,
    }
    return render(request, template_name="invoice/show_template.html", context=context)


def generate_fac(request):
    context = {
        "title": "Show invoice",
        "contracts": Contragent.objects.filter(is_active=True),
    }
    if request.method == "POST":
        request_data = {
            "fak_type": request.POST.get("fak_type"),
            "fak_pay": request.POST.get("fak_pay"),
            "contragent_id": Contragent.objects.get(
                id=request.POST.get("contragent_id")
            ),
            "name": request.POST.get("name"),
            "q": int(request.POST.get("q")),
            "brut": Decimal(request.POST.get("brut")),
            "dds": int(request.POST.get("dds")),
        }

        f_eleements = FakElelements(
            text=request_data["name"],
            kol=request_data["q"],
            brutna_cena=request_data["brut"],
            dds=int(request_data["dds"]),
        )
        f_eleements.save()
        fak_id = FakId.objects.filter(number=f_eleements.faktura_id.number)[0]
        fak_id.contract_id = request_data["contragent_id"]

        fak_id.save()

        return redirect("show_invoice", id_=fak_id.id)

    return render(request, template_name="invoice/generate_fac.html", context=context)


def main_page_for_invoice(request):
    return render(request, template_name="invoice/invoice_base.html")


def generate_and_edit_owner(request):
    """
    If owner is already configure, return data to form for edin, another way
    show empty form.
    """
    form = forms.OwnerForm(
        request.POST or None, instance=OwnerModel.objects.get(id=1) or None
    )
    context = {"title": "Owner Configuration", "form": form}
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("index")
    return render(request, template_name="invoice/config_owner.html", context=context)


class ContractView(ListView):
    model = Contragent
    context_object_name = "contracts"
    template_name = "invoice/contract.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Contracts"
        return context


class ConctractNew(CreateView):
    model = Contragent
    fields = "name town address mol bulstat idmum is_active".split()
    template_name = "invoice/new_contract.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(*kwargs)
        context["title"] = "Create New Conctract"
        return context

    def get_success_url(self):
        return reverse("contracts")


class ContractEdit(UpdateView):
    model = Contragent
    fields = "name town address mol bulstat idmum is_active".split()
    template_name = "invoice/new_contract.html"

    def get_success_url(self):
        return reverse("contracts")


class ShowAllInvoices(ListView):
	model = FakId
	template_name = 'invoice/show_all_invoices.html'
	context_object_name = 'invoices'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Show All Invoices"
		return context



