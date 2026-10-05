import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from accounts.forms.password_reset_form import PasswordResetRequestForm, SetNewPasswordForm
from accounts.models import User
from core.services.email_service import send_password_reset_email

logger = logging.getLogger('accounts')


def password_reset_request_view(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_link = request.build_absolute_uri(f'/accounts/reset-password/{uid}/{token}/')

                send_password_reset_email(to_email=user.email, reset_link=reset_link)
                logger.info(f'لینک بازیابی رمز برای {email} ارسال شد.')
            except User.DoesNotExist:
                logger.warning(f'درخواست بازیابی رمز برای ایمیل ثبت‌نشده: {email}')
                # عمداً پیام یکسان نشان می‌دهیم تا وجود/عدم‌وجود ایمیل لو نرود

            messages.success(request, 'اگر این ایمیل در سیستم ثبت باشد، لینک بازیابی برای آن ارسال می‌شود.')
            return redirect('accounts:login')
    else:
        form = PasswordResetRequestForm()

    return render(request, 'accounts/password_reset_request.html', {'form': form})


def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None or not default_token_generator.check_token(user, token):
        messages.error(request, 'لینک بازیابی نامعتبر یا منقضی شده است.')
        return redirect('accounts:login')

    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['password'])
            user.save()
            logger.info(f'رمز عبور کاربر {user.phone} با موفقیت بازیابی شد.')
            messages.success(request, 'رمز عبور شما با موفقیت تغییر کرد. اکنون وارد شوید.')
            return redirect('accounts:login')
    else:
        form = SetNewPasswordForm()

    return render(request, 'accounts/password_reset_confirm.html', {'form': form})