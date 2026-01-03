from django.shortcuts import render
# Create your views here.

from django.http import HttpResponse  
from accounts.models import User, Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import JsonResponse
from .form import Profileform
from django.contrib.auth import get_user_model
from django.db.models import Q,F
from connectpro.utility import get_daily_connection_stats
from .models import Connection
from django.contrib import messages


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

    limit, remaining = get_daily_connection_stats(request.user)

    connections = Connection.objects.filter(Q(from_user=request.user) | Q(to_user=request.user))
    active_connections = connections.filter(status="accepted")
    active_count = active_connections.count()

    context = {
        "profile_user": profile_user,
        "profile": profile_obj,
        "form": form,
        "active_connections": active_count,
        "limit": limit,
        "remaining" : remaining,
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

User = get_user_model()

@login_required
def discover(request):
    search_query = request.GET.get("q","").strip()

    users = User.objects.exclude(id=request.user.id).select_related("profile")

    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(profile__headline__icontains=search_query)|
            Q(profile__location__icontains=search_query)
        )
    
    connections = Connection.objects.filter(Q(from_user=request.user) | Q(to_user=request.user))
    
    connection_map = {}
    for conn in connections:
        other = conn.to_user if conn.from_user == request.user else conn.from_user
        direction = "sent" if conn.from_user == request.user else "received"
        connection_map[other.id] = (conn, direction)
    
    for person in users:
        data = connection_map.get(person.id)
        if data:
            person.existing_connection = data[0]
            person.connection_direction =data[1]
        else:
            person.existing_connection = None
            person.connection_direction = None

    limit, remaining = get_daily_connection_stats(request.user)

    active_connections = connections.filter(status="accepted")

    return render(request,"connectpro/discover.html", {
        "users" : users,
        "search_query": search_query,
        "remaining": remaining,
        "active_connections": active_connections,
    }) 

@login_required
def connect(request, username):
    to_user = get_object_or_404(User, username = username)

    limit, remaning = get_daily_connection_stats(request.user)

    if remaning == 0:
        messages.error(request, "Daily connection limit reached. Upgrade your plan for more.")
        return redirect("connectpro:discover")
    Connection.objects.create(from_user = request.user,to_user=to_user)
    messages.success(request, f"Connection request sent to {to_user.username}.")
    return redirect("connectpro:discover")

@login_required
def respond_connection(request, connection_id):
    """
    Accept or decline a received connection request.
    """
    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect("connectpro:discover")

    connection = get_object_or_404(Connection, id=connection_id)

    # Only the receiver can respond
    if connection.to_user != request.user:
        messages.error(request, "You are not allowed to respond to this request.")
        return redirect("connectpro:discover")

    action = request.POST.get("action")

    if action == "accept":
        connection.status = Connection.Status.ACCEPTED
        connection.save()
        messages.success(request, f"You are now connected with {connection.from_user.username}.")
    elif action == "decline":
        connection.status = Connection.Status.DECLINED
        connection.save()
        messages.info(request, f"You declined the connection request from {connection.from_user.username}.")
    else:
        messages.error(request, "Invalid action.")

    # Redirect back to the page user came from
    next_url = request.POST.get("next") or "connectpro:discover"
    return redirect(next_url)

# networking/views.py
from django.shortcuts import render
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def profile_detail(request, user_id):
    """
    Show full profile of a user.
    """
    person = get_object_or_404(User, id=user_id)
    return render(request, "connectpro/profile.html", {
        "person": person
    })

@login_required
def connections_json(request):
    connections = Connection.objects.filter(
        from_user=request.user,
        status="accepted"
    ).select_related("to_user", "to_user__profile")

    data = [
        {
            "id": c.to_user.id,
            "username": c.to_user.username,
            "headline": c.to_user.profile.headline,
            "avatar": c.to_user.profile.profile_picture.url
                      if c.to_user.profile.profile_picture else ""
        }
        for c in connections
    ]

    return JsonResponse({"connections": data})