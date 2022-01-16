from django.urls import path

from .views import LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView

app_name = 'authentication'
urlpatterns = [
    path('users/register/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    # users/update/ пока не доработаны
    # path('users/update/', UserRetrieveUpdateAPIView.as_view())
]