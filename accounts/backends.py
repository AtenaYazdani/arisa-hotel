from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class UsernameBackend(ModelBackend):
    """
    مخصوص ورود به پنل ادمین جنگو (/admin) — فقط بر اساس username.
    ورود کاربران عادی به سایت اصلی، جدا و بر پایه‌ی phone پیاده‌سازی می‌شود.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            return None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None