import random
import logging
from django.utils import timezone
from datetime import timedelta
from core.models import OTPCode
from core.services.sms_service import send_sms

logger = logging.getLogger('core')

OTP_VALIDITY_MINUTES = 2


def generate_and_send_otp(phone: str, purpose: str) -> OTPCode:
    """
    یک کد ۶ رقمی جدید برای شماره و هدف مشخص می‌سازد،
    کدهای قبلیِ استفاده‌نشده‌ی همان شماره و هدف را باطل می‌کند،
    و کد جدید را پیامک می‌کند.
    """
    OTPCode.objects.filter(phone=phone, purpose=purpose, is_used=False).update(is_used=True)
    code = str(random.randint(100000, 999999))
    expires_at = timezone.now() + timedelta(minutes=OTP_VALIDITY_MINUTES)
    otp = OTPCode.objects.create(
        phone=phone,
        code=code,
        purpose=purpose,
        expires_at=expires_at,
    )

    send_sms(phone, f'کد تأیید شما: {code}\nاعتبار: {OTP_VALIDITY_MINUTES} دقیقه\nهتل آریسا')

    logger.info(f'کد OTP برای شماره {phone} با هدف {purpose} ساخته و ارسال شد.')
    return otp


def verify_otp(phone: str, purpose: str, entered_code: str) -> bool:
    """
    بررسی می‌کند آیا کد واردشده برای این شماره و هدف معتبر است.
    در صورت معتبر بودن، کد را مصرف‌شده علامت می‌زند و True برمی‌گرداند.
    """
    otp = OTPCode.objects.filter(
        phone=phone,
        purpose=purpose,
        code=entered_code,
        is_used=False,
    ).order_by('-created_at').first()
    if not otp:
        logger.warning(f'تلاش ناموفق تأیید OTP برای شماره {phone} (هدف: {purpose}) - کد نامعتبر یا استفاده‌شده.')
        return False
    if otp.expires_at < timezone.now():
        logger.warning(f'تلاش ناموفق تأیید OTP برای شماره {phone} (هدف: {purpose}) - کد منقضی‌شده.')
        return False
    otp.is_used = True
    otp.save()
    logger.info(f'کد OTP برای شماره {phone} (هدف: {purpose}) با موفقیت تأیید شد.')
    return True