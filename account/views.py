import folium
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.gis.geos import Point
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView
from .forms import SignupForm, UserProfileUpdateForm
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


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileUpdateForm
    # fields = ['first_name', 'last_name', 'email', 'username', 'phone_number', 'address', 'location']
    template_name = 'user/update_profile.html'
    success_url = reverse_lazy('profile')
    login_url = '/account/user/signin/'

    def get_initial(self):
        initial = super().get_initial()
        location = self.request.user.location
        initial['longitude'] = location.x
        initial['latitude'] = location.y
        return initial

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.pk})

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        latitude = form.cleaned_data.get("latitude")
        longitude = form.cleaned_data.get("longitude")
        self.request.user.location = Point(float(longitude), float(latitude))
        self.request.user.save()
        return super().form_valid(form)


class UsersLocationView(LoginRequiredMixin, TemplateView):
    template_name = 'user/user_location.html'
    login_url = '/account/user/signin/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.filter(location__isnull=False)
        if not users.exists():
            return context

        map_center = [users.first().location.y, users.first().location.x]
        map_obj = folium.Map(location=map_center, zoom_start=10)

        for user in users:
            marker = folium.Marker([user.location.y, user.location.x]).add_to(map_obj)
            info_html = f'<h3>{user.first_name} {user.last_name}</h3><br><h5>{user.address}</h5'
            marker.add_child(folium.Popup(info_html, max_width=300))
            marker.add_to(map_obj)

        context['map'] = map_obj._repr_html_()
        return context
