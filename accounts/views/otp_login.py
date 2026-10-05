import logging
from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login
from django.contrib import messages
from accounts.forms.otp_login_form import OTPLoginRequestForm, OTPLoginVerifyForm
from accounts.models import User
from core.services.otp_service import generate_and_send_otp, verify_otp

logger = logging.getLogger('accounts')


def otp_login_request_view(request):
    if request.method == 'POST':
        form = OTPLoginRequestForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']

            if not User.objects.filter(phone=phone, phone_verified=True).exists():
                messages.error(request, 'کاربری با این شماره یافت نشد.')
                return render(request, 'accounts/otp_login_request.html', {'form': form})

            generate_and_send_otp(phone=phone, purpose='login')
            request.session['otp_login_phone'] = phone
            request.session['otp_login_next'] = request.GET.get('next') or request.POST.get('next', '')

            logger.info(f'کد ورود OTP برای شماره {phone} ارسال شد.')
            return redirect('accounts:otp_login_verify')
    else:
        form = OTPLoginRequestForm()

    return render(request, 'accounts/otp_login_request.html', {'form': form})

def otp_login_verify_view(request):
    phone = request.session.get('otp_login_phone')

    if not phone:
        messages.error(request, 'ابتدا شماره تماس خود را وارد کنید.')
        return redirect('accounts:otp_login_request')

    if request.method == 'POST':
        if 'resend' in request.POST:
            generate_and_send_otp(phone=phone, purpose='login')
            messages.success(request, 'کد جدید ارسال شد.')
            return render(request, 'accounts/otp_login_verify.html')

        form = OTPLoginVerifyForm(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data['code']
            is_valid = verify_otp(phone=phone, purpose='login', entered_code=entered_code)

            if is_valid:
                user = User.objects.get(phone=phone)
                django_login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                del request.session['otp_login_phone']
                next_url = request.session.pop('otp_login_next', None)
                logger.info(f'ورود موفق با OTP: {phone}')
                if next_url:
                    return redirect(next_url)
                return redirect('core:index')
            else:
                messages.error(request, 'کد وارد شده صحیح نیست یا منقضی شده است.')

    return render(request, 'accounts/otp_login_verify.html')