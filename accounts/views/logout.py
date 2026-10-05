import logging
from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect

logger = logging.getLogger('accounts')


def logout_view(request):
    phone = request.user.phone if request.user.is_authenticated else None
    django_logout(request)
    logger.info(f'خروج کاربر: {phone}')
    return redirect('core:index')