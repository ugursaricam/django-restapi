from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Kennwort eingeben',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Kennwort bestätigen',
        'class': 'form-control',
    }))
    
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'company_name', 'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Vornamen eingeben'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Nachname eingeben'
        self.fields['company_name'].widget.attrs['placeholder'] = 'Firmenname eingeben'
        self.fields['email'].widget.attrs['placeholder'] = 'E-Mail Adresse eingeben'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Telefonnummer eingeben'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')


        if password != confirm_password:
            raise forms.ValidationError(
                "Password did not match!"
            )