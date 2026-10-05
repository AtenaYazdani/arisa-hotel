from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, phone, email, first_name, last_name, national_code, password=None, **extra_fields):
        if not phone:
            raise ValueError('شماره تماس الزامی است')
        if not email:
            raise ValueError('ایمیل الزامی است')

        email = self.normalize_email(email)
        user = self.model(
            phone=phone,
            email=email,
            first_name=first_name,
            last_name=last_name,
            national_code=national_code,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email, first_name, last_name, national_code, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('phone_verified', True)
        extra_fields.setdefault('role', 'admin_main')

        if not extra_fields.get('username'):
            raise ValueError('نام کاربری برای ادمین الزامی است')

        return self.create_user(
            phone=phone,
            email=email,
            first_name=first_name,
            last_name=last_name,
            national_code=national_code,
            password=password,
            **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('normal', 'کاربر عادی'),
        ('admin_main', 'ادمین اصلی'),
        ('admin_reservation', 'ادمین رزرواسیون'),
    ]
    GENDER_CHOICES = [
        ('male', 'مرد'),
        ('female', 'زن'),
    ]
    # اطلاعات پایه
    first_name = models.CharField(max_length=50, verbose_name='نام')
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی')
    national_code = models.CharField(max_length=10, unique=True, verbose_name='کد ملی')
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    phone = models.CharField(max_length=11, unique=True, verbose_name='شماره تماس')
    # نام کاربری: اجباری برای ادمین‌ها (ورود به پنل ادمین)، اختیاری برای کاربر عادی
    username = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name='نام کاربری')
    # اطلاعات تکمیلی پروفایل
    address = models.TextField(blank=True, null=True, verbose_name='آدرس')
    birth_date = models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name='عکس پروفایل')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True, verbose_name='جنسیت')
    # نقش کاربر
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='normal', verbose_name='نقش')
    # وضعیت تأیید شماره
    phone_verified = models.BooleanField(default=False, verbose_name='شماره تأیید شده')

    # وضعیت حساب
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_staff = models.BooleanField(default=False, verbose_name='دسترسی پنل ادمین جنگو')

    # امنیت ورود
    failed_login_attempts = models.PositiveSmallIntegerField(default=0, verbose_name='تلاش‌های ناموفق ورود')
    locked_until = models.DateTimeField(blank=True, null=True, verbose_name='قفل تا')

    # یادداشت داخلی ادمین
    admin_comment = models.TextField(blank=True, null=True, verbose_name='یادداشت داخلی ادمین')

    # زمان‌ها
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت‌نام')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین ویرایش')

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'national_code', 'username']

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.phone})'

class AdminUser(User):
    class Meta:
        proxy = True
        verbose_name = 'ادمین'
        verbose_name_plural = 'مدیریت ادمین‌ها'