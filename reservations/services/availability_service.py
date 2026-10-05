from reservations.models import Reservation


def is_room_available(room_type, check_in, check_out) -> bool:
    """
    بررسی می‌کند آیا برای نوع اتاق مشخص‌شده، در بازه‌ی check_in تا check_out
    ظرفیت خالی وجود دارد یا خیر.
    """
    overlapping_count = Reservation.objects.filter(
        room_type=room_type,
        check_in__lt=check_out,
        check_out__gt=check_in,
    ).exclude(status='cancelled').count()

    return overlapping_count < room_type.quantity