from django.urls import path
from accounts.views.register import register_view
from accounts.views.verify_register import verify_register_view
from accounts.views.login import login_view
from accounts.views.logout import logout_view
from accounts.views.password_reset import password_reset_request_view, password_reset_confirm_view
from accounts.views.otp_login import otp_login_request_view, otp_login_verify_view
from accounts.views.profile import profile_view
app_name = 'accounts'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('verify-register/', verify_register_view, name='verify_register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('reset-password/', password_reset_request_view, name='password_reset_request'),
    path('reset-password/<uidb64>/<token>/', password_reset_confirm_view, name='password_reset_confirm'),
    path('otp-login/', otp_login_request_view, name='otp_login_request'),
    path('otp-login/verify/', otp_login_verify_view, name='otp_login_verify'),
    path('profile/', profile_view, name='profile'),
]