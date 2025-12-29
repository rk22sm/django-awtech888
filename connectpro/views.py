from django.shortcuts import render
# Create your views here.

from django.http import HttpResponse  
from accounts.models import User, Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .form import Profileform



def discover(request):
    return render(request, "connectpro/discover.html",{'user':request.user})

@login_required
def profile(request, pk=None):
    profile_user = request.user
    if pk:
        profile_user = get_object_or_404(User, pk=pk)
    profile_obj, _ = Profile.objects.get_or_create(user=profile_user)

    if pk and request.user != profile_user:
        Profile.objects.filter(pk=profile_obj.pk).update(profile_views=F("profile_views") + 1)
        profile_obj.refresh_from_db(fields=["profile_views"])

    if request.method == "POST":
        return redirect("connectpro:edit_profile")
    form = Profileform(instance=request.user.profile)
    context = {
        "profile_user": profile_user,
        "profile": profile_obj,
        "form": form,
    }
   
    return render(request, 'connectpro/profile.html', context)

@login_required
def edit_profile(request):
    user_profile = request.user.profile
   

    if request.method == "POST":
        form = Profileform(
            request.POST,
            request.FILES,
            instance=user_profile
        )
        if form.is_valid():
            form.save()
            return redirect("connectpro:profile")
        else:
            print(form.errors)
    else:
        form = Profileform(instance=user_profile)

    return render(request, "connectpro/profile.html", {
        "user_profile": user_profile,
        "form": form
    })

