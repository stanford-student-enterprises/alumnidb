import logging

import requests

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import login
from django.contrib import auth

from alumnidb.linkedin import tasks, models
from alumnidb.linkedin.lib import linkedin_api

logger = logging.getLogger(__name__)

def connect(request):
    if request.GET.get("code"):
        code = request.GET.get("code")
        token = linkedin_api.get_auth_token(code, "http://%s/linkedin/connect" % request.get_host())
        profile_info = linkedin_api.get_profile(token, fields=["first-name", "last-name", "id", "headline", "picture-url", "email-address", "site-standard-profile-request"])
        logger.error(profile_info)

        user, created = models.UserProfile.objects.get_or_create(linkedin_id=profile_info['id'], oauth_code=code)
        user = auth.authenticate(username=str(user.linkedin_id), password="ab")
        login(request, user)

        user.first_name = profile_info['firstName']

        if 'lastName' in profile_info:
            user.last_name = profile_info['lastName']

        if 'pictureUrl' in profile_info:
            user.picture_url = profile_info['pictureUrl']

        if 'emailAddress' in profile_info:
            user.email = profile_info['emailAddress']

        if 'headline' in profile_info:
            user.headline = profile_info['headline']

        if 'siteStandardProfileRequest' in profile_info:
            user.linkedin_profile_url = profile_info['siteStandardProfileRequest']['url']

        user.oauth_token = token
        user.oauth_code = code
        user.save()

        tasks.crawl_linkedin(user)

        if request.GET.get("next"):
            return HttpResponseRedirect(request.GET.get("next"))
        return HttpResponseRedirect('/db/profile/')
    else:
        return HttpResponse(status=404)


def authenticate(request):
    url = linkedin_api.get_auth_code_url("http://%s/linkedin/connect" % request.get_host())
    #if request.GET.get("next"):
    #   url += "?next=%s" % request.GET.get("next")

    logger.error(url)
    return HttpResponseRedirect(url)