from django.urls import path
from .views import UserSignupView, UserSigninView, UserSignOutView, UserProfileView


urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('signin/', UserSigninView.as_view(), name='signin'),
    path('signout/', UserSignOutView.as_view(), name='signout'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
]
