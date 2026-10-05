from django import forms


class OTPLoginRequestForm(forms.Form):
    phone = forms.CharField(label='شماره تماس', max_length=11)


class OTPLoginVerifyForm(forms.Form):
    code = forms.CharField(label='کد تأیید', max_length=6)