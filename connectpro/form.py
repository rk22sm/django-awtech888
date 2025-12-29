from django import forms
from accounts.models import Profile, User

class Profileform(forms.ModelForm): 
    class Meta:
        model = Profile
        fields = ['headline', 'bio','skills','experience','location','profile_picture']

