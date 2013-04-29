from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db.models import Q

from alumnidb.linkedin.models import UserProfile
from alumnidb.linkedin.forms import UserProfileForm

def home(request):
    return render_to_response("database/home.html")

def all(request):
    users = UserProfile.objects.all().order_by("last_name")

    data = {"users": users,
            "title": "All Employees",}

    return render_to_response("database/list.html", data, context_instance=RequestContext(request))

def current(request):
    users = UserProfile.objects.filter(is_current=True).order_by("last_name")

    data = {"users": users,
            "title": "All Employees",}

    return render_to_response("database/list.html", data, context_instance=RequestContext(request))

def my_profile(request):
    user = request.user

    return render_to_response("database/profile.html", {"user": user}, context_instance=RequestContext(request))

def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/db/profile/')
    else:
        form = UserProfileForm(instance=user)

    return render_to_response("database/edit_profile.html", {"form": form}, context_instance=RequestContext(request))

def profile(request, user_id):
    user = get_object_or_404(UserProfile, pk=user_id)

    return render_to_response("database/profile.html", {"user": user}, context_instance=RequestContext(request))

def search(request):
    q = request.GET.get("q", "")
    results = []

    for qw in q.split():
        results.extend(UserProfile.objects.filter(
            Q(first_name__icontains=qw) |
            Q(last_name__icontains=qw) |
            Q(headline__icontains=qw) |
            Q(sse_position__icontains=qw) |
            Q(sse_year__icontains=qw)
        ))
    
    return render_to_response("database/list.html", {"users": results, "title": "Search results for '%s'" % q},
                            context_instance=RequestContext(request))