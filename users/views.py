from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm, ProfilePictureForm
from django.contrib.auth.views import LoginView, LogoutView

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class CustomLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('product_list')

class CustomLogoutView(LogoutView):
    next_page = '/'
