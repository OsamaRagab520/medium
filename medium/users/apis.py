from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from medium.api.permissions import IsOwner
from medium.users.models import User
from medium.users.selectors import get_user
from medium.users.services import UserService


class CreateUserApi(APIView):
    permission_classes = [AllowAny]

    class InputSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()
        name = serializers.CharField()
        email = serializers.EmailField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = UserService()
        service.create_user(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class DetailUserApi(APIView):
    class OutputSerializer(serializers.Serializer):
        username = serializers.CharField()
        name = serializers.CharField()
        email = serializers.EmailField()

    def get(self, request, user_id):
        user = get_user(User, id=user_id)
        serializer = self.OutputSerializer(user)
        return Response(serializer.data)


class UpdateUserApi(APIView):

    permission_classes = [IsOwner]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        email = serializers.EmailField(required=False)

    def post(self, request, user_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = UserService()
        service.update_user(
            id=user_id,
            data=serializer.validated_data,
        )
        return Response(status=status.HTTP_200_OK)
