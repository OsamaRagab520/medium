from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

# from medium.api.permissions import IsOwner
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
    # TODO Remove when JWT authentication is implemented
    permission_classes = [AllowAny]

    class OutputSerializer(serializers.Serializer):
        username = serializers.CharField()
        name = serializers.CharField()
        email = serializers.EmailField()

    def get(self, request, user_id):
        user = get_user(user_id)
        serializer = self.OutputSerializer(user)
        return Response(serializer.data)


class UpdateUserApi(APIView):

    # TODO Remove when JWT authentication is implemented
    permission_classes = [AllowAny]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        email = serializers.EmailField(required=False)
        password = serializers.CharField(required=False)

    def post(self, request, user_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_user(user_id)

        service = UserService()
        service.update_user(
            user=user,
            fetched_by=request.user,
            data=serializer.validated_data,
        )
        return Response(status=status.HTTP_200_OK)
