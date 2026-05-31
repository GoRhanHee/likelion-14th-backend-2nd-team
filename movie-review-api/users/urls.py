from django.urls import path
from .views import SignupView, MyProfileView, LogoutView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='api-signup'), 
    path('profile/', MyProfileView.as_view(), name='api-profile'),
    path('logout/', LogoutView.as_view(), name='api-logout'), 
]