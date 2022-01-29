from .views import CreateConferenceAPIView, AddMemberAPIView, DeleteMemberAPIView, DeleteConferenceAPIView
from django.urls import path

app_name = 'conference'
urlpatterns = [
    path('create/', CreateConferenceAPIView.as_view()),
    path('add-member/', AddMemberAPIView.as_view()),
    path('delete-conference/', DeleteConferenceAPIView.as_view()),
    path('delete-member/', DeleteMemberAPIView.as_view()),
]