from django.shortcuts import render
from django.http import HttpResponse  
from django.contrib.auth.decorators import login_required
from allauth.account.views import LoginView, SignupView,LogoutView
from .form import CustomLoginForm, CustomSignupForm
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect

# Create your views here.
def index(request):  
   return render(request, 'index.html')

class CustomLoginView(LoginView):
    #template_name = 'account/login.html'
    def get_success_url(self):
        return reverse_lazy('connectpro:profile')

class CustomSignupView(SignupView):
    template_name = 'account/signup.html'


def forgot_pass(request):
    return HttpResponse("hello")

def Mylogout(request):
    logout(request)
    return redirect('accounts:index')
