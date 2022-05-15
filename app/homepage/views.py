

from django.views.generic import FormView

from .forms import SubnetForm
from .tasks import add_function, nmap_analyze


class ContactFormView(FormView):
    form_class = SubnetForm
    template_name = "pages/contact_form.html"
    success_url = "/"

    def form_valid(self, form):
        form.save()
        self.start_nmap_analyze(form.cleaned_data)

        return super().form_valid(form)

    def start_nmap_analyze(self, valid_data):
        subnet_ip = valid_data["subnet_ip"]
        mask = valid_data["mask"]

        nmap_analyze.delay(subnet_ip, mask)


    def add(self, x, y):
        add_function.delay(x, y)