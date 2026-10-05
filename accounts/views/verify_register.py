import logging
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from accounts.models import User
from core.services.otp_service import generate_and_send_otp, verify_otp
from core.services.email_service import send_welcome_email

logger = logging.getLogger('accounts')

REGISTER_TIMEOUT_MINUTES = 5


def verify_register_view(request):
    phone = request.session.get('pending_phone')

    if not phone:
        messages.error(request, 'ابتدا ثبت‌نام کنید.')
        return redirect('accounts:register')

    try:
        user = User.objects.get(phone=phone, phone_verified=False)
    except User.DoesNotExist:
        messages.error(request, 'حساب کاربری یافت نشد یا قبلاً تأیید شده است.')
        del request.session['pending_phone']
        return redirect('accounts:register')

    # چک مهلت ۵ دقیقه‌ای کلی ثبت‌نام
    if timezone.now() > user.created_at + timedelta(minutes=REGISTER_TIMEOUT_MINUTES):
        logger.info(f'ثبت‌نام کاربر {phone} به دلیل انقضای مهلت ۵ دقیقه‌ای حذف شد.')
        user.delete()
        del request.session['pending_phone']
        messages.error(request, 'مهلت شما به پایان رسید. لطفاً دوباره ثبت‌نام کنید.')
        return redirect('accounts:register')

    if request.method == 'POST':
        if 'resend' in request.POST:
            generate_and_send_otp(phone=phone, purpose='register')
            messages.success(request, 'کد جدید ارسال شد.')
            return render(request, 'accounts/verify_register.html')

        entered_code = request.POST.get('code', '').strip()
        is_valid = verify_otp(phone=phone, purpose='register', entered_code=entered_code)

        if is_valid:
            user.phone_verified = True
            user.save()

            send_welcome_email(to_email=user.email, first_name=user.first_name)

            del request.session['pending_phone']
            logger.info(f'ثبت‌نام کاربر {phone} با موفقیت تأیید شد.')

            messages.success(request, 'ثبت‌نام شما تأیید شد. اکنون می‌توانید وارد شوید.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'کد وارد شده صحیح نیست یا منقضی شده است.')

    return render(request, 'accounts/verify_register.html')