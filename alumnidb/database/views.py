from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
    return render_to_response("database/home.html")

def all(request):
    users = User.objects.all().order_by("last_name")

    return render_to_response("database/list.html", {"users": users})

def my_profile(request):
    user = request.user

    return render_to_response("database/profile.html", {"user": user}, context_instance=RequestContext(request))

def edit_profile(request):
    pass

def profile(request, user_id):
    pass