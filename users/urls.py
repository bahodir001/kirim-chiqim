from django.urls import path
from .views import (signup_view, login_view, logout_view, profile_view,
                    RegisterView, LogoutView, LoginView, family_group_view, verify_email_view  )

urlpatterns = [
    path('register/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('family/', family_group_view, name='family'),

    # API url-lar oldingidek qoladi
    path('api/register/', RegisterView.as_view(), name='api-register'),
    path('api/login/', LoginView.as_view(), name='api-login'),
    path('api/logout/', LogoutView.as_view(), name='api-logout'),
    path('profile/', profile_view, name='profile'),
    path('verify/', verify_email_view, name='verify-email'),

]
