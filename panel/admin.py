from django import forms
from django.contrib import admin
from accounts.admin import AdminMessageForm
from reservations.models import Reservation
from panel.models import AdminMessage
from accounts.models import User
from panel.admin_sites import reservation_admin_site
import jdatetime


def jalali(date_value):
    if not date_value:
        return '-'
    if hasattr(date_value, 'date'):
        date_value = date_value.date()
    return jdatetime.date.fromgregorian(date=date_value).strftime('%Y/%m/%d')
@admin.register(Reservation, site=reservation_admin_site)
class ReservationPanelAdmin(admin.ModelAdmin):
    list_display = ('confirmation_code', 'user', 'room_type', 'jalali_check_in', 'jalali_check_out', 'status')
    list_filter = ('status', 'check_in', 'check_out')
    search_fields = ('confirmation_code', 'user__first_name', 'user__last_name', 'user__phone')
    readonly_fields = ('confirmation_code', 'user', 'room_type', 'check_in', 'check_out', 'created_at')
    list_editable = ('status',)
    list_display_links = ('confirmation_code',)
    fieldsets = (
        (None, {'fields': ('confirmation_code', 'user', 'room_type', 'check_in', 'check_out', 'status')}),
        ('جزئیات', {'fields': ('note', 'created_at')}),
    )

    def jalali_check_in(self, obj):
        return jalali(obj.check_in)
    jalali_check_in.short_description = 'تاریخ ورود'

    def jalali_check_out(self, obj):
        return jalali(obj.check_out)
    jalali_check_out.short_description = 'تاریخ خروج'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

@admin.register(AdminMessage, site=reservation_admin_site)
class AdminMessagePanelAdmin(admin.ModelAdmin):
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

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True


#============================================
from django import forms
from django.contrib import admin, messages
from django.core.mail import send_mail
from django.shortcuts import render
from panel.models import NewsletterSubscriber


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


@admin.register(NewsletterSubscriber, site=reservation_admin_site)
class NewsletterSubscriberPanelAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    actions = [send_newsletter_email]