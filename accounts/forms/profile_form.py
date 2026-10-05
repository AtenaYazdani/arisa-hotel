from django import forms
from accounts.models import User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'address', 'birth_date', 'gender', 'profile_image']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }