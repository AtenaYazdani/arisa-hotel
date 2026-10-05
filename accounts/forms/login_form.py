from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='نام کاربری', max_length=50)
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)