from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import ConferenceJSONRenderer, MemberJSONRenderer
from .serializers import CreateConferenceSerializer, AddMemberSerializer


# Create your views here.
class CreateConferenceAPIView(APIView):
    """
    Разрешить всем аутентифицированным пользователям доступ к данному эндпоинту.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateConferenceSerializer

    renderer_classes = (ConferenceJSONRenderer,)

    def post(self, request):
        conference = self.serializer_class(data=[request.data.get('conference', {}), request.user])
        conference.is_valid(raise_exception=True)
        conference.save()
        print(f'-- conference.data = {conference.data}')

        return Response(conference.data, status=status.HTTP_201_CREATED)


class AddMemberAPIView(APIView):
    """
    Разрешить всем аутентифицированным пользователям доступ к данному эндпоинту.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = AddMemberSerializer

    renderer_classes = (MemberJSONRenderer,)

    def post(self, request):
        data = request.data.get('conference', {})
        # print(f'-- data["request"] = {data["request"]}')
        is_admin, conference_id = self.serializer_class(data=data)
        member = Members.objects.create(is_admin=is_admin, user_id=request.user.ID, conference_id=conference_id)
        member.is_valid(raise_exception=True)
        member.save()
        print(f'-- member.data = {member.data}')

        return Response(member.data, status=status.HTTP_201_CREATED)
