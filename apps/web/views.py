from django.views.generic.base import TemplateView

# Create your views here.

class IndexView(TemplateView):
    template_name = 'app/login/login.html'

class RegisterView(TemplateView):
    template_name = 'app/login/register.html'