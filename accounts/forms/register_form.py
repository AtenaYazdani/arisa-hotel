from django import forms
from accounts.models import User


class RegisterForm(forms.Form):
    first_name = forms.CharField(label='نام', max_length=50)
    last_name = forms.CharField(label='نام خانوادگی', max_length=50)
    national_code = forms.CharField(label='کد ملی', max_length=10)
    email = forms.EmailField(label='ایمیل')
    phone = forms.CharField(label='شماره تماس', max_length=11)
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='تکرار رمز عبور', widget=forms.PasswordInput)
    username = forms.CharField(label='نام کاربری', max_length=50)

    def clean_national_code(self):
        national_code = self.cleaned_data['national_code']
        if User.objects.filter(national_code=national_code).exists():
            raise forms.ValidationError('این کد ملی قبلاً ثبت شده است.')
        return national_code

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('این ایمیل قبلاً ثبت شده است.')
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError('این شماره تماس قبلاً ثبت شده است.')
        return phone

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('این نام کاربری قبلاً استفاده شده است.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('رمز عبور و تکرار آن یکسان نیستند.')

        return cleaned_data