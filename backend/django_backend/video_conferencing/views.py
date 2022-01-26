from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import ConferenceJSONRenderer, MemberJSONRenderer
from .serializers import CreateConferenceSerializer, AddMemberSerializer,\
    DeleteMemberSerializer, DeleteConferenceSerializer
from .models import Members, Conference


# Create your views here.
class CreateConferenceAPIView(APIView):
    """
    Разрешить всем аутентифицированным пользователям доступ к данному эндпоинту.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateConferenceSerializer

    renderer_classes = (ConferenceJSONRenderer,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data.get('conference', {}))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(f"-- conference.data['ID'] = {serializer.data['ID']}")
        conference = Conference.objects.get(ID=serializer.data['ID'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeleteConferenceAPIView(APIView):
    """
    Разрешить всем аутентифицированным пользователям доступ к данному эндпоинту.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = DeleteConferenceSerializer

    renderer_classes = (ConferenceJSONRenderer,)

    def delete(self, request):
        data = request.data.get('conference', {})
        user = request.user
        ID = data.get('ID', None)
        print(f'-- data = {data}')
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

        try:
            members = Members.objects.all().filter(user_id=user.ID, conference_id=ID)
            print(f'-- len(members) = {len(members)}')
            for member in members:
                print(f'-- member = {member}')
                print(f'-- member.ID = {member.ID}')
                print(f'-- member.is_admin = {member.is_admin}')
                print(f'-- member.conference_id = {member.conference_id}')
                if member.is_admin is True:
                    print('-- user is admin')
                    break
            else:
                print('user is not admin')
                return Response({'detail': 'Error. User is not admin'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                conference = Conference.objects.get(ID=ID)
                print(f'-- conference = {conference}')
                print(f'-- conference.ID = {conference.ID}')
                print(f'-- conference.url = {conference.url}')
                print('-- before delete')
                conference.delete()
                print('-- after delete')
                return Response({'detail': 'Conference was deleted successfully!'}, status=status.HTTP_200_OK)
            except:
                return Response({'detail': 'Error. Conference not found.'}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({'detail': 'Error. User is not admin'}, status=status.HTTP_400_BAD_REQUEST)


class AddMemberAPIView(APIView):
    """
    Разрешить всем аутентифицированным пользователям доступ к данному эндпоинту.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = AddMemberSerializer

    renderer_classes = (MemberJSONRenderer,)

    def post(self, request):
        data = request.data.get('member', {})
        # # print(f'-- data["request"] = {data["request"]}')
        data['user_id'] = request.user.ID
        # print(f'-- data = {data}')
        member = self.serializer_class(data=data)
        # conference = Conference.objects.get(ID=conference_id)
        # member = Members.objects.create(is_admin=is_admin, user_id=request.user, conference_id=conference)
        member.is_valid(raise_exception=True)
        member.save()
        # print(f'-- member.data = {member.data}')
        return Response(member.data, status=status.HTTP_201_CREATED)


class DeleteMemberAPIView(APIView):
    """
    Разрешить всем аутентифицированным пользователям доступ к данному эндпоинту.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = DeleteMemberSerializer

    renderer_classes = (MemberJSONRenderer,)

    def delete(self, request):
        data = request.data.get('member', {})
        user = request.user
        conference_id = data.get('conference_id', None)
        ID = data.get('ID', None)
        data['user_id'] = user.ID
        print(f'-- data = {data}')
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

        try:
            members = Members.objects.all().filter(user_id=user.ID, conference_id=conference_id)
            print(f'-- len(members) = {len(members)}')
            for member in members:
                print(f'-- member = {member}')
                print(f'-- member.user_id.ID = {member.user_id.ID}')
                print(f'-- member.ID = {member.ID}')
                print(f'-- member.is_admin = {member.is_admin}')
                print(f'-- member.conference_id = {member.conference_id}')
                if member.is_admin is True or member.user_id == user.ID:
                    print('-- user is admin')
                    break
            else:
                print('user is not admin')
                return Response({'detail': 'Error. User is not admin'}, status=status.HTTP_400_BAD_REQUEST)

            member = Members.objects.get(ID=ID)
            print(f'-- member = {member}')
            print(f'-- member.ID = {member.ID}')
            print(f'-- member.is_admin = {member.is_admin}')
            print(f'-- member.conference_id = {member.conference_id}')
            print('-- before delete')
            member.delete()
            print('-- after delete')
            return Response({'detail': 'Member was deleted successfully!'}, status=status.HTTP_200_OK)
        except:
            return Response({'detail': 'Error. Member not found.'}, status=status.HTTP_400_BAD_REQUEST)
