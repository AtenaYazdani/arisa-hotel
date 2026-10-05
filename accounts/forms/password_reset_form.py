from django import forms


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label='ایمیل')


class SetNewPasswordForm(forms.Form):
    password = forms.CharField(label='رمز عبور جدید', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='تکرار رمز عبور جدید', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('رمز عبور و تکرار آن یکسان نیستند.')

        return cleaned_data