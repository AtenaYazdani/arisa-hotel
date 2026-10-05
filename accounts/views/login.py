import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from accounts.forms.login_form import LoginForm
from accounts.models import User

logger = logging.getLogger('accounts')

MAX_FAILED_ATTEMPTS = 10
LOCK_DURATION_MINUTES = 60


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
                logger.warning(f'تلاش ورود با نام کاربری ثبت‌نشده: {username}')
                return render(request, 'accounts/login.html', {'form': form})
            # چک قفل بودن حساب
            if user.locked_until and timezone.now() < user.locked_until:
                remaining = user.locked_until.strftime('%H:%M')
                messages.error(request, f'حساب شما قفل است. لطفاً تا ساعت {remaining} صبر کنید.')
                logger.warning(f'تلاش ورود به حساب قفل‌شده: {username}')
                return render(request, 'accounts/login.html', {'form': form})
            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user is not None:
                user.failed_login_attempts = 0
                user.locked_until = None
                user.save()

                django_login(request, authenticated_user)
                logger.info(f'ورود موفق کاربر: {username}')

                next_url = request.POST.get('next') or request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('core:index')
            else:
                user.failed_login_attempts += 1

                if user.failed_login_attempts >= MAX_FAILED_ATTEMPTS:
                    user.locked_until = timezone.now() + timedelta(minutes=LOCK_DURATION_MINUTES)
                    user.failed_login_attempts = 0
                    user.save()
                    messages.error(request, 'به دلیل تلاش‌های ناموفق زیاد، حساب شما به مدت ۱ ساعت قفل شد.')
                    logger.warning(f'حساب کاربر {username} به دلیل تلاش‌های ناموفق زیاد قفل شد.')
                else:
                    user.save()
                    messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
                    logger.warning(f'تلاش ناموفق ورود برای نام کاربری {username} (تلاش {user.failed_login_attempts})')

                return render(request, 'accounts/login.html', {'form': form})
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})