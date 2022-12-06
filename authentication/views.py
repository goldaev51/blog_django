from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views import generic
from .forms import RegistrationForm


class RegistrationFormView(generic.FormView):
    template_name = 'registration/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('blog:posts-list')

    def form_valid(self, form):
        user = form.save()
        user = authenticate(self.request, username=user.username, password=form.cleaned_data.get('password1'))
        login(self.request, user)
        return super(RegistrationFormView, self).form_valid(form)
