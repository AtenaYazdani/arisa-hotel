import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.forms.profile_form import ProfileForm

logger = logging.getLogger('accounts')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            logger.info(f'اطلاعات پروفایل کاربر {request.user.phone} ویرایش شد.')
            messages.success(request, 'اطلاعات با موفقیت ذخیره شد.')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form, 'active_tab': 'info'})