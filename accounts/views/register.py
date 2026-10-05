import logging
from django.shortcuts import render, redirect
from accounts.forms.register_form import RegisterForm
from accounts.models import User
from core.services.otp_service import generate_and_send_otp

logger = logging.getLogger('accounts')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            user = User.objects.create_user(
                phone=data['phone'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                national_code=data['national_code'],
                username=data['username'],
                password=data['password'],
            )

            generate_and_send_otp(phone=user.phone, purpose='register')

            request.session['pending_phone'] = user.phone

            logger.info(f'کاربر جدید ثبت‌نام کرد و منتظر تأیید OTP است: {user.phone}')

            return redirect('accounts:verify_register')
        else:
            logger.warning(f'تلاش ناموفق ثبت‌نام - خطاهای فرم: {form.errors}')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})