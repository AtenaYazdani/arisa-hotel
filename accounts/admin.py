from django import forms
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import User, AdminUser
from panel.models import AdminMessage
import jdatetime
from django.core.mail import send_mail
from django.shortcuts import render
from panel.models import NewsletterSubscriber
from django.contrib.admin import SimpleListFilter
from django.http import HttpResponse
from reservations.services.pdf_service import build_pdf_table



def jalali(date_value):
    if not date_value:
        return '-'
    if hasattr(date_value, 'date'):
        date_value = date_value.date()
    return jdatetime.date.fromgregorian(date=date_value).strftime('%Y/%m/%d')
# ==========================
# فرم‌های سفارشی کاربر (با هش صحیح پسورد)
# ==========================

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('phone', 'username', 'email', 'first_name', 'last_name', 'national_code')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = '__all__'

class HasReservationFilter(SimpleListFilter):
    title = 'وضعیت رزرو'
    parameter_name = 'has_reservation'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'دارای رزرو'),
            ('no', 'بدون رزرو'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(reservations__isnull=False).distinct()
        if self.value() == 'no':
            return queryset.filter(reservations__isnull=True)
        return queryset
class UserEmailForm(forms.Form):
    subject = forms.CharField(label='موضوع ایمیل', max_length=200)
    body = forms.CharField(label='متن ایمیل', widget=forms.Textarea(attrs={'rows': 10}))
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)


def send_email_to_users(modeladmin, request, queryset):
    queryset = queryset.exclude(email='')
    if 'apply' in request.POST:
        form = UserEmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            emails = list(queryset.values_list('email', flat=True))
            send_mail(subject, body, 'noreply@arisahotel.com', emails, fail_silently=False)
            modeladmin.message_user(request, f'ایمیل به {len(emails)} کاربر ارسال شد.', messages.SUCCESS)
            return None
    else:
        form = UserEmailForm(initial={'_selected_action': queryset.values_list('pk', flat=True)})

    return render(request, 'accounts/send_user_email.html', {
        'users': queryset,
        'form': form,
    })


send_email_to_users.short_description = 'ارسال ایمیل به کاربران انتخاب‌شده'


def export_users_pdf(modeladmin, request, queryset):
    headers = ['نام و نام‌خانوادگی', 'نام کاربری', 'کد ملی', 'شماره تماس']
    rows = []
    for user in queryset:
        rows.append([
            f'{user.first_name} {user.last_name}',
            user.username,
            user.national_code,
            user.phone,
        ])
    pdf_buffer = build_pdf_table(
        title='فهرست کاربران انتخاب‌شده',
        headers=headers,
        rows=rows,
    )
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="users_report.pdf"'
    return response


export_users_pdf.short_description = 'دریافت PDF کاربران انتخاب‌شده'
# ==========================
# مدیریت کاربران عادی (User)
# ==========================

class UserAdmin(BaseUserAdmin):
    model = User
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('phone', 'username', 'first_name', 'last_name', 'email', 'role', 'is_active', 'is_staff', 'jalali_created_at')
    list_filter = ('role', 'is_active', 'is_staff', HasReservationFilter)
    search_fields = ('phone', 'username', 'first_name', 'last_name', 'email', 'national_code')
    ordering = ('-created_at',)
    actions = [send_email_to_users, export_users_pdf]

    @admin.display(description='تاریخ ایجاد')
    def jalali_created_at(self, obj):
        return jalali(obj.created_at)

    fieldsets = (
        (None, {'fields': ('phone', 'username', 'password')}),
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name', 'national_code', 'email', 'address', 'birth_date', 'gender', 'profile_image')}),
        ('نقش و دسترسی', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('وضعیت تأیید و امنیت', {'fields': ('phone_verified', 'failed_login_attempts', 'locked_until')}),
        ('یادداشت ادمین', {'fields': ('admin_comment',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'username', 'email', 'first_name', 'last_name', 'national_code', 'password1', 'password2'),
        }),
    )


admin.site.register(User, UserAdmin)


# ==========================
# مدیریت ادمین‌ها (Proxy Model)
# ==========================

class AdminUserManager(BaseUserAdmin):
    model = AdminUser
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('username', 'first_name', 'last_name', 'phone', 'role', 'is_active')
    list_filter = ('role',)
    search_fields = ('username', 'first_name', 'last_name', 'phone')

    fieldsets = (
        (None, {'fields': ('phone', 'username', 'password')}),
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name', 'national_code', 'email')}),
        ('نقش و دسترسی', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'username', 'email', 'first_name', 'last_name', 'national_code', 'role', 'password1', 'password2'),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(role__in=['admin_main', 'admin_reservation'])

    def save_model(self, request, obj, form, change):
        if obj.role in ('admin_main', 'admin_reservation'):
            obj.is_staff = True
        if obj.role == 'admin_main':
            obj.is_superuser = True
        super().save_model(request, obj, form, change)


admin.site.register(AdminUser, AdminUserManager)


# ==========================
# مدیریت پیام‌های ادمین
# ==========================

class AdminMessageForm(forms.ModelForm):
    class Meta:
        model = AdminMessage
        fields = ('receiver', 'text')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['receiver'].queryset = User.objects.filter(role__in=['admin_main', 'admin_reservation'])


class AdminMessageAdmin(admin.ModelAdmin):
    form = AdminMessageForm
    list_display = ('sender', 'receiver', 'created_at', 'is_read')
    list_filter = ('is_read',)
    readonly_fields = ('sender', 'created_at')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.sender = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(receiver=request.user) | qs.filter(sender=request.user)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        if obj and obj.receiver == request.user and not obj.is_read:
            obj.is_read = True
            obj.save()
        return super().change_view(request, object_id, form_url, extra_context)


admin.site.register(AdminMessage, AdminMessageAdmin)


# ==========================
# سفارشی‌سازی فرم ورود پنل ادمین (نمایش "نام کاربری")
# ==========================

class AdminLoginForm(AuthenticationForm):
    username = forms.CharField(label='نام کاربری')


admin.site.login_form = AdminLoginForm
admin.site.login_template = None


# ==========================
# محدودسازی دسترسی /admin/ فقط به admin_main
# ==========================

def custom_has_permission(request):
    return (
        request.user.is_active
        and request.user.is_staff
        and request.user.role == 'admin_main'
    )


admin.site.has_permission = custom_has_permission


# ==========================
# نمایش نوتیفیکیشن پیام خوانده‌نشده + قالب داشبورد سفارشی
# ==========================

def custom_each_context(request):
    context = original_each_context(request)
    if request.user.is_authenticated:
        context['unread_message_count'] = AdminMessage.objects.filter(
            receiver=request.user, is_read=False
        ).count()
        context['messages_url'] = '/admin/panel/adminmessage/'
    return context


original_each_context = admin.site.each_context
admin.site.each_context = custom_each_context
admin.site.index_template = 'admin/custom_index.html'


#============================

class NewsletterEmailForm(forms.Form):
    subject = forms.CharField(label='موضوع ایمیل', max_length=200)
    body = forms.CharField(label='متن ایمیل', widget=forms.Textarea(attrs={'rows': 10}))
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)


def send_newsletter_email(modeladmin, request, queryset):
    if 'apply' in request.POST:
        form = NewsletterEmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            emails = list(queryset.values_list('email', flat=True))
            send_mail(subject, body, 'noreply@arisahotel.com', emails, fail_silently=False)
            modeladmin.message_user(request, f'ایمیل به {len(emails)} نفر ارسال شد.', messages.SUCCESS)
            return None
    else:
        form = NewsletterEmailForm(initial={'_selected_action': queryset.values_list('pk', flat=True)})

    return render(request, 'panel/send_newsletter_email.html', {
        'subscribers': queryset,
        'form': form,
    })


send_newsletter_email.short_description = 'ارسال ایمیل به ایمیل‌های انتخاب‌شده'


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberPanelAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    actions = [send_newsletter_email]

