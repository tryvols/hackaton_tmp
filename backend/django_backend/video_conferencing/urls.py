from .views import CreateConferenceAPIView, AddMemberAPIView
from django.urls import path

app_name = 'conference'
urlpatterns = [
    path('create/', CreateConferenceAPIView.as_view()),
    path('add-member/', AddMemberAPIView.as_view())
    # path('connect/', ),
    # path('delete-member/', )
]