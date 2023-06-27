from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.gis.geos import Point
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView
from .forms import SignupForm
from .models import User


class UserSignupView(CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('signin')
    template_name = 'user/signup.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        longitude = form.cleaned_data.pop('longitude')
        latitude = form.cleaned_data.pop('latitude')
        if latitude and longitude:
            user.location = Point(float(longitude), float(latitude))
        user.save()
        return redirect(self.success_url)


class UserSigninView(LoginView):
    template_name = 'user/signin.html'
    # success_url = reverse_lazy('signup')

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        user = form.get_user()
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Invalid username or password.')
            return self.form_invalid(form)


class UserSignOutView(LogoutView):
    next_page = reverse_lazy('signin')


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user/user_profile.html'
    context_object_name = 'user'
    login_url = '/account/user/signin/'
