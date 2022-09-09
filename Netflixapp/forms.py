from django.forms import ModelForm
from Netflixapp.models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['uuid']