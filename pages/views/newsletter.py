from django.shortcuts import redirect
from django.contrib import messages
from panel.models import NewsletterSubscriber


def newsletter_subscribe_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            obj, created = NewsletterSubscriber.objects.get_or_create(email=email)
            if created:
                messages.success(request, 'ایمیل شما با موفقیت ثبت شد.')
            else:
                messages.info(request, 'این ایمیل قبلاً ثبت شده است.')
    return redirect(request.META.get('HTTP_REFERER', '/'))