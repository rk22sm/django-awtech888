from django.shortcuts import render
from django.http import HttpResponse  
from django.contrib.auth.decorators import login_required
from allauth.account.views import LoginView, SignupView,LogoutView
from .form import CustomLoginForm, CustomSignupForm
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404, redirect, render
from .models import Notification
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
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

@login_required
def mark_notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def notification_list(request):
    notifications = request.user.notifications.all().order_by("-created_at")
    return render(request, "base/notifications.html", {
        "notifications": notifications
    })
@csrf_exempt
@login_required

def notifications_mark_all_read(request):
    if request.method == "POST":
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({"status": "ok"})