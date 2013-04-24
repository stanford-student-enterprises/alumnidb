from celery import task
import datetime

import requests

from django.conf import settings

from alumnidb.linkedin.models import UserProfile

import logging, sys

from alumnidb.linkedin.lib import linkedin_api

logger = logging.getLogger(__name__)


    
@task()
def crawl_linkedin(user):
    fields = ["id","first-name","last-name","headline","email-address","picture-url"]
    json_data = linkedin_api.get_profile(user.oauth_token, fields)
    parse_user_data(user, json_data)

def parse_user_data(user, json_data):
    update_user(user, json_data)
    user.save()

def update_user(user, json_data):
    user.linkedin_id = json_data["id"]
    user.first_name = json_data["firstName"]

    if 'lastName' in json_data:
        user.last_name = json_data['lastName']

    if 'pictureUrl' in json_data:
        user.picture_url = json_data['pictureUrl']

    if 'emailAddress' in json_data:
        user.email = json_data['emailAddress']

    if 'headline' in json_data:
        user.headling = json_data['headline']
