from django import forms
from django.contrib.admin import AdminSite
from django.contrib.auth.forms import AuthenticationForm


class ReservationLoginForm(AuthenticationForm):
    username = forms.CharField(label='نام کاربری')

class ReservationAdminSite(AdminSite):
    site_header = 'پنل مدیریت رزرواسیون - هتل آریسا'
    site_title = 'پنل رزرواسیون'
    index_title = 'خوش آمدید'
    login_form = ReservationLoginForm
    index_template = 'reservation_admin/index.html'

    def has_permission(self, request):
        return (
            request.user.is_active
            and request.user.is_authenticated
            and request.user.role in ('admin_reservation', 'admin_main')
        )

    def each_context(self, request):
        context = super().each_context(request)
        if request.user.is_authenticated:
            from panel.models import AdminMessage
            context['unread_message_count'] = AdminMessage.objects.filter(
                receiver=request.user, is_read=False
            ).count()
            context['messages_url'] = '/panel/reservations/panel/adminmessage/'
        return context


reservation_admin_site = ReservationAdminSite(name='reservation_admin')