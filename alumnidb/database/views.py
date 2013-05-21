from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db.models import Q

from alumnidb.linkedin.models import UserProfile, SSEPosition, Experience
from alumnidb.linkedin.forms import UserProfileForm, AdminUserProfileForm, SSEPositionForm

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

    return profile(request, user.pk)

def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/db/profile/')
    else:
        form = UserProfileForm(instance=user)

    return render_to_response("database/edit_profile.html", {"form": form, "action":"/db/profile/edit/"}, context_instance=RequestContext(request))

def add_sse_position(request, user_id):
    user = get_object_or_404(UserProfile, pk=int(user_id))
    if user != request.user and not request.user.is_superuser:
        return HttpResponse(status=401)

    if request.method == 'POST':
        form = SSEPositionForm(request.POST)
        if form.is_valid():
            position = form.save(commit=False)
            position.user = user
            position.save()
            return HttpResponseRedirect('/db/profile/')
    else:
        form = SSEPositionForm()

    return render_to_response("database/add_sse_position.html", 
                            {"form": form},
                            context_instance=RequestContext(request))

def edit_sse_position(request, user_id, position_id):
    user = get_object_or_404(UserProfile, pk=int(user_id))
    position = get_object_or_404(SSEPosition, pk=int(position_id))
    if user != request.user and not request.user.is_superuser:
        return HttpResponse(status=401)
    if position.user != user:
        return HttpResponse(status=401)

    if request.method == 'POST':
        form = SSEPositionForm(request.POST, instance=position)
        if form.is_valid():
            position = form.save(commit=False)
            position.user = user
            position.save()
            return HttpResponseRedirect('/db/profile/')
    else:
        form = SSEPositionForm(instance=position)

    return render_to_response("database/edit_sse_position.html", 
                            {"form": form},
                            context_instance=RequestContext(request))

def delete_sse_position(request, user_id, position_id):
    user = get_object_or_404(UserProfile, pk=int(user_id))
    position = get_object_or_404(SSEPosition, pk=int(position_id))
    if user != request.user and not request.user.is_superuser:
        return HttpResponse(status=401)
    if position.user != user:
        return HttpResponse(status=401)

    position.delete()

    return HttpResponseRedirect("/db/profile/%d/" % user.pk)

def admin_edit_profile(request, user_id):
    user = get_object_or_404(UserProfile, pk=int(user_id))
    if not request.user.is_superuser:
        return HttpResponse(status=401)

    if request.method == 'POST':
        form = AdminUserProfileForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/db/profile/%s/' % user_id)
    else:
        form = AdminUserProfileForm(instance=user)

    return render_to_response("database/edit_profile.html", {"form": form, "action":"/db/profile/%s/edit/" % user_id}, context_instance=RequestContext(request))

def profile(request, user_id):
    user = get_object_or_404(UserProfile, pk=user_id)

    sse_positions = SSEPosition.objects.filter(user=user).order_by("-start_year")
    experiences = Experience.objects.filter(user=user)

    return render_to_response("database/profile.html", 
                            {"user": user,
                            "sse_positions": sse_positions,
                            "experiences": experiences}, 
                            context_instance=RequestContext(request))

def search(request):
    q = request.GET.get("q", "")
    results = set()

    for qw in q.split():
        results |= set(UserProfile.objects.filter(
            Q(first_name__icontains=qw) |
            Q(last_name__icontains=qw) |
            Q(headline__icontains=qw)
        ))

        q_object = Q(start_year__lte=qw)
        q_object.add(Q(end_year__gte=qw) | Q(title__icontains=qw), Q.AND)
        sse_positions = SSEPosition.objects.filter(q_object)

        for sse_position in sse_positions:
            results.add(sse_position.user)

        experiences = Experience.objects.filter(
            Q(title__icontains=qw) |
            Q(organization__icontains=qw)
        )
        for experience in experiences:
            results.add(experience.user)

    
    return render_to_response("database/list.html", {"users": results, "title": "Search results for '%s'" % q},
                            context_instance=RequestContext(request))