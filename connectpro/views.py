from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse  



# @login_required
def profile(request):
    # You can pass user details to the template if needed
    return render(request, 'connectpro/profile.html', {'user': request.user})