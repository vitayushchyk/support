import uuid

from django.core.cache import cache
from django.urls import reverse
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
        activation_key = uuid.uuid4()
        cache.set(f"{activation_key}", user.pk, timeout=60 * 60)
        activation_url = reverse(
            "users-activation", kwargs={"activation_key": activation_key}
        )
        send_activation_mail.delay(
            recipient=user.email,
            activation_link=self.request.build_absolute_uri(activation_url),
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
    def get(self, request, activation_key, *args, **kwargs):
        user_id = cache.get(f"{activation_key}")
        if user_id is None:
            return Response(
                {"error": "Invalid activation key"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        user.is_active = True
        user.save()
        cache.delete(f"{activation_key}")
        return Response({"message": "Your email is successfully activated"})
