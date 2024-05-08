from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Role, User
from users.serializers import UserCreateSerializer, UserRetrieveUpdateDestroySerializer
from users.tasks import send_activation_mail


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer: UserCreateSerializer):
        super().perform_create(serializer)
        user: User = serializer.instance
        activation_key = user.activationkey_set.all()[0]
        send_activation_mail.delay(
            recipient=user.email,
            activation_link=f"Please activate your account: {activation_key.key}",
        )


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveUpdateDestroySerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        if request.user.role != Role.ADMIN:
            raise PermissionDenied("Arrrrr, you shall not pass!!!! ")
        return super().delete(request, *args, **kwargs)


class UserActivateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        activation_key = request.data.get("key")
        if not activation_key:
            return Response(
                {"error": "Missing activation key"}, status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.get(activationkey__key=activation_key)
        user.is_active = True
        user.activationkey_set.all().delete()
        user.save()
        return Response({"message": "Your email is successfully activated"})
