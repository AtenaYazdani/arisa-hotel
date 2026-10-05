from django import forms


class ReservationForm(forms.Form):
    check_in = forms.DateField(
        label='تاریخ ورود',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    check_out = forms.DateField(
        label='تاریخ خروج',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    guest_names = forms.CharField(
        label='اسامی مهمانان (اختیاری، هر نام در یک خط)',
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
    )
    note = forms.CharField(
        label='توضیحات',
        widget=forms.Textarea(attrs={'rows': 2}),
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out:
            from django.utils import timezone
            today = timezone.now().date()
            if check_in < today:
                raise forms.ValidationError('تاریخ ورود نمی‌تواند در گذشته باشد.')
            if check_out <= check_in:
                raise forms.ValidationError('تاریخ خروج باید بعد از تاریخ ورود باشد.')

        return cleaned_data