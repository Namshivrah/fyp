from django import forms
from django.forms import ModelChoiceField, ModelForm
from .models import Voters, Candidates
#create forms here

class VoterRegistrationForm(forms.ModelForm):
    class Meta:
        model = Voters
<<<<<<< HEAD
<<<<<<< HEAD
        fields = ['first_name', 'middle_name', 'last_name', 'gender', 'date_of_birth', 'nin_number', 'phone_contact', 'voter_type', 'Polling_station', 'fingerprint_xtics']
=======
        fields = ['first_name', 'middle_name', 'last_name', 'gender', 'date_of_birth', 'nin_number', 'phone_contact', 'voter_type', 'Polling_station']
>>>>>>> 3409599e8033f19433aae308b612cf1988cd5850
=======
        fields = ['first_name', 'middle_name', 'last_name', 'gender', 'date_of_birth', 'nin_number', 'phone_contact', 'voter_type', 'Polling_station']
>>>>>>> 3409599e8033f19433aae308b612cf1988cd5850
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }       

class CandidateRegistrationForm(forms.ModelForm):
    class Meta:
        model = Candidates
        fields = ['profile_pic','first_name', 'middle_name', 'last_name', 'gender', 'political_party', 'post_aspired_for']
