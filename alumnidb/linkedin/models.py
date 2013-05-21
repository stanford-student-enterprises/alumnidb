from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import simplejson
from django.core import serializers
from django.conf import settings

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

    def create_superuser(self, linkedin_id, password, **other_fields):
        user = self.model(linkedin_id=linkedin_id)

        user.set_password(password)

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


class UserProfile(AbstractBaseUser, PermissionsMixin):
    linkedin_id = models.CharField(max_length=255, unique=True)
    linkedin_profile_url = models.CharField(max_length=255, blank=True, null=True)
    oauth_token = models.CharField(max_length=255, null=True, blank=True)
    oauth_code = models.CharField(max_length=255, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    picture_url = models.CharField(max_length=255, blank=True, null=True)
    headline = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    sse_email = models.CharField(max_length=255, blank=True, null=True, verbose_name="SSE Email")
    is_current = models.BooleanField(default=True)
    receive_emails = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = LinkedInUserManager()

    USERNAME_FIELD = 'linkedin_id'

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

    def last_sse_position(self):
        sse_positions = SSEPosition.objects.filter(user=self).order_by("-start_year")
        if sse_positions.count():
            return sse_positions[0]
        else:
            return None

    def sse_positions(self):
        return SSEPosition.objects.filter(user=self).order_by("-start_year")

class SSEPosition(models.Model):
    start_year = models.CharField(max_length=4, choices=settings.YEAR_CHOICES)
    end_year = models.CharField(max_length=4, choices=settings.YEAR_CHOICES)
    title = models.CharField(max_length=255)
    user = models.ForeignKey("UserProfile")

    def __unicode__(self):
        return "%s - %s from %s to %s" % (self.user, self.title, self.start_year, self.end_year)

class Experience(models.Model):
    linkedin_id = models.CharField(max_length=50, null=True, default=None, blank=True)
    organization = models.CharField(max_length=100)
    start_year = models.IntegerField(null=True, blank=True)
    start_month = models.IntegerField(null=True, blank=True)
    end_year = models.IntegerField(null=True, blank=True)
    end_month = models.IntegerField(null=True, blank=True)
    summary = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey("UserProfile")

    class Meta:
        ordering = ["start_year", "start_month"]

    def __unicode__(self):
        return "%s - %s from %s" % (self.user, self.organization, self.start_year)

    def json_dict(self):
        d = {}
        d["linkedin_id"] = self.linkedin_id
        d["id"] = self.pk
        d["type"] = "experience"
        if self.start_year:
            d["start_year"] = self.start_year
        if self.start_month:
            d["start_month"] = self.start_month
        if self.end_year:
            d["end_year"] = self.end_year
        if self.end_month:
            d["end_month"] = self.end_month
        if self.summary:
            d["summary"] = self.summary
        if self.title :
            d["title"] = self.title
        if self.organization:
            d["organization"] = self.organization
        
        return d