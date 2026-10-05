import logging

logger = logging.getLogger('core')


def send_sms(phone: str, message: str) -> bool:
    """
    ارسال پیامک. فعلاً به‌صورت تستی روی کنسول چاپ می‌شود.
    در آینده، بدنه‌ی این تابع می‌تواند به یک سرویس واقعی پیامک وصل شود
    بدون نیاز به تغییر در جاهای دیگر پروژه.
    """
    print(f'--- SMS به {phone} ---')
    print(message)
    print('------------------------')

    logger.info(f'پیامک برای شماره {phone} ارسال شد.')
    return True