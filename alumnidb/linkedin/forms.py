from django.forms import ModelForm

from alumnidb.linkedin.models import UserProfile, SSEPosition

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('linkedin_id', 'oauth_token', 'oauth_code', 'date_joined', 'last_login', 'headline', 'password', 'picture_url', 'email', 'is_staff', 'is_superuser','groups', 'user_permissions','linkedin_profile_url',)

class AdminUserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('linkedin_id', 'oauth_token', 'oauth_code', 'date_joined', 'last_login', 'headline', 'password', 'picture_url', 'is_staff','groups', 'user_permissions','linkedin_profile_url',)

class SSEPositionForm(ModelForm):
    class Meta:
        model = SSEPosition
        exclude = ('user',)