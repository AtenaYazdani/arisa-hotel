import logging
from django.core.mail import send_mail
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings

logger = logging.getLogger('core')

EMAIL_SIGNATURE = '\n\n---\nگروه هتلینگ‌های آریسا'

HOTEL_RULES = """
- ورود به هتل از ساعت ۱۴:۰۰ و خروج تا ساعت ۱۲:۰۰ ظهر
- ارائه کارت شناسایی معتبر الزامی است
- استعمال دخانیات در اتاق‌ها ممنوع است
- حیوانات خانگی پذیرفته نمی‌شوند
"""


class ReadableConsoleEmailBackend(BaseEmailBackend):
    """
    نسخه‌ی خوانا برای نمایش ایمیل در کنسول (مخصوص محیط توسعه).
    برخلاف EmailBackend پیش‌فرض جنگو، متن را بدون رمزنگاری MIME/base64 چاپ می‌کند.
    """

    def send_messages(self, email_messages):
        for message in email_messages:
            print('=' * 60)
            print(f'به: {", ".join(message.to)}')
            print(f'موضوع: {message.subject}')
            print('-' * 60)
            print(message.body)
            print('=' * 60)
        return len(email_messages)


def send_welcome_email(to_email: str, first_name: str) -> bool:
    subject = 'به هتل آریسا خوش آمدید'
    message = (
        f'{first_name} عزیز،\n\n'
        'ثبت‌نام شما در سایت هتل آریسا با موفقیت انجام شد.\n'
        'از همراهی شما خوشحالیم و امیدواریم تجربه‌ی خوبی داشته باشید.'
        f'{EMAIL_SIGNATURE}'
    )

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])
    logger.info(f'ایمیل خوش‌آمدگویی برای {to_email} ارسال شد.')
    return True


def send_password_reset_email(to_email: str, reset_link: str) -> bool:
    subject = 'بازیابی رمز عبور - هتل آریسا'
    message = (
        'برای بازیابی رمز عبور خود، روی لینک زیر کلیک کنید:\n\n'
        f'{reset_link}\n\n'
        'اگر این درخواست را شما ثبت نکرده‌اید، این پیام را نادیده بگیرید.'
        f'{EMAIL_SIGNATURE}'
    )

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])
    logger.info(f'ایمیل بازیابی رمز برای {to_email} ارسال شد.')
    return True


def send_reservation_confirmation_email(
    to_email: str,
    room_name: str,
    check_in,
    check_out,
    nights_count: int,
    confirmation_code: str,
) -> bool:
    subject = 'تأیید رزرو - هتل آریسا'
    message = (
        'رزرو شما با موفقیت ثبت شد.\n\n'
        f'نوع اتاق: {room_name}\n'
        f'تاریخ ورود: {check_in}\n'
        f'تاریخ خروج: {check_out}\n'
        f'مدت اقامت: {nights_count} شب\n\n'
        f'کد تأیید رزرو شما: {confirmation_code}\n\n'
        'قوانین هتل:\n'
        f'{HOTEL_RULES}'
        f'{EMAIL_SIGNATURE}'
    )

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])
    logger.info(f'ایمیل تأیید رزرو برای {to_email} ارسال شد.')
    return True