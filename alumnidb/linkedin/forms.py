from django.forms import ModelForm

from alumnidb.linkedin.models import UserProfile

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('linkedin_id', 'oauth_token', 'oauth_code', 'date_joined', 'last_login', 'headline', 'password', 'picture_url', 'email',)
