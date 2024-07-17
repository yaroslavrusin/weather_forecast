from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import RegisterUserForm


# Create your views here.
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')
