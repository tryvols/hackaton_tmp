import random
from rest_framework import serializers
from .models import Conference, Members
from authentication.models import User
from django.contrib.auth import authenticate


def create_conf_code():
    chars = '1234567890qwertyuiopasdfghjklzxcvbnm'
    code = ''.join([random.choice(chars) for _ in range(0, random.randint(6, 12))])
    return code


class CreateConferenceSerializer(serializers.ModelSerializer):
    """ Сериализация создания конференции. """

    ID = serializers.IntegerField(read_only=True)
    url = serializers.CharField(max_length=13, read_only=True)

    class Meta:
        model = Conference
        # Перечислить все поля, которые могут быть включены в запрос
        # или ответ, включая поля, явно указанные выше.
        fields = ['ID', 'url']

    def create(self, data):
        print(f'--- start func "create" in class CreateConferenceSerializer ---')
        conference = Conference.objects.create(url=create_conf_code())
        print(f'-- conference.url = {conference.url}')
        return conference


class AddMemberSerializer(serializers.ModelSerializer):
    """ Сериализация создания конференции. """

    ID = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Members
        # Перечислить все поля, которые могут быть включены в запрос
        # или ответ, включая поля, явно указанные выше.
        fields = ['ID', 'user_id', 'conference_id', 'is_admin']

    def create(self, data):
        print(f'--- start func "create" in class AddMemberSerializer ---')
        print(f'-- data = {data}')
        conference_id = data.get('conference_id', None)
        print(f'-- conference_id = {conference_id}')
        is_admin = data.get('is_admin', None)
        print(f'-- is_admin = {is_admin}')
        return conference_id, is_admin
