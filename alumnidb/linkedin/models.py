from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import simplejson
from django.core import serializers

class LinkedInUserManager(BaseUserManager):
    def create(self, linkedin_id, oauth_code):
        if not linkedin_id or not oauth_code:
            raise ValueError("Users must be created with a linkedin in and an oauth code")

        user = self.model(
            linkedin_id=linkedin_id,
            oauth_code=oauth_code
        )

        user.set_password("ab")

        user.save(using=self._db)
        return user

    def get_or_create(self, linkedin_id=None, oauth_code=None):
        try:
            user = self.get(linkedin_id=linkedin_id)
            user.oauth_code = oauth_code
            user.save()
            return user, False
        except:
            return self.create(linkedin_id, oauth_code), True


class UserProfile(AbstractBaseUser):
    linkedin_id = models.CharField(max_length=255, unique=True)
    linkedin_profile_url = models.CharField(max_length=255, blank=True, null=True)
    oauth_token = models.CharField(max_length=255)
    oauth_code = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    picture_url = models.CharField(max_length=255, blank=True, null=True)
    headline = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    sse_position = models.CharField(max_length=255, blank=True, null=True, verbose_name="SSE Position")
    sse_year = models.CharField(max_length=255, blank=True, null=True, verbose_name="SSE Year")
    sse_email = models.CharField(max_length=255, blank=True, null=True, verbose_name="SSE Email")
    is_current = models.BooleanField(default=True)
    receive_emails = models.BooleanField(default=True)

    objects = LinkedInUserManager()

    USERNAME_FIELD = 'linkedin_id'
    REQUIRED_FIELDS = ['oauth_code']

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def primary_email(self):
        if self.is_current:
            if self.sse_email:
                return self.sse_email
            else:
                return self.email
        else:
            return self.email
        return None    