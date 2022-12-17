from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from .forms import UpdateUserForm

decorators = [cache_page(20), vary_on_cookie]

@method_decorator(decorators, 'dispatch')
class UserPublicProfile(generic.DetailView):
    model = User
    template_name = 'user_profile/public_profile.html'


@login_required()
def show_user_profile(request):
    user = User.objects.get(pk=request.user.id)
    return render(request, 'user_profile/user_profile.html', {'user': user})


@login_required()
def update_user_profile(request):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('user_profile:user-profile')
    else:
        form = UpdateUserForm(instance=request.user)
    return render(request, 'user_profile/update_user_profile.html', {'form': form})
