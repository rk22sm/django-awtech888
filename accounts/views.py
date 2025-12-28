from django.shortcuts import render
from django.http import HttpResponse  
from django.contrib.auth.decorators import login_required
from allauth.account.views import LoginView, SignupView,LogoutView
from .form import CustomLoginForm, CustomSignupForm
from django.urls import reverse_lazy

# Create your views here.
def home(request):  
    return HttpResponse("hello")

class CustomLoginView(LoginView):
    #template_name = 'account/login.html'
    def get_success_url(self):
        return reverse_lazy('profile')

class CustomSignupView(SignupView):
    template_name = 'account/signup.html'


def forgot_pass(request):
    return HttpResponse("hello")

class CustomLogoutView(LogoutView):
    next_page = ''
