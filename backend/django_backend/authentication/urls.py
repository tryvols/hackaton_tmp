from .views import LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView
from django.urls import path

app_name = 'authentication'
urlpatterns = [
    path('users/register/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('users/update/', UserRetrieveUpdateAPIView.as_view()),
]