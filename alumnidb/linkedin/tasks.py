from celery import task
import datetime

import requests

from django.conf import settings

from alumnidb.linkedin.models import UserProfile, Experience

import logging, sys

from alumnidb.linkedin.lib import linkedin_api

logger = logging.getLogger(__name__)


@task()
def crawl_linkedin(user):
    fields = ["id","first-name","last-name","headline","email-address","picture-url","positions"]
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

    if 'positions' in json_data:
        if 'values' in json_data['positions']:
            parse_experiences(user, json_data["positions"]["values"])

def parse_experiences(user, positions_data):
    for individual_position_data in positions_data:
            parse_experience(user, individual_position_data)
    user.save()

def parse_experience(user, individual_position_data):
    experience, created = Experience.objects.get_or_create(linkedin_id=individual_position_data["id"],
                                                                user=user)
    experience.linkedin_id = individual_position_data["id"]
    if "startDate" in individual_position_data:
        if "year" in individual_position_data["startDate"]:
            experience.start_year = individual_position_data["startDate"]["year"]
        if "month" in individual_position_data["startDate"]:
            experience.start_month = individual_position_data["startDate"]["month"]
    if "endDate" in individual_position_data:
        experience.end_year = individual_position_data["endDate"]["year"]
        if "month" in individual_position_data["endDate"]:
            experience.end_month = individual_position_data["endDate"]["month"]
    if "summary" in individual_position_data:
        experience.summary = individual_position_data["summary"]
    if "title" in individual_position_data:
        experience.title = individual_position_data["title"]
    if "company" in individual_position_data:
        experience.organization = individual_position_data["company"]["name"]
    
    experience.save()

    return experience
