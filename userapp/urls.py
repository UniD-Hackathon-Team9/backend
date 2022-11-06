from django.urls import path

from userapp.views import UserPersonalityCreateView

app_name = 'users'

urlpatterns = [
    path('me', UserPersonalityCreateView.as_view(), name="me")
]
