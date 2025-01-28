import secrets
from base64 import b64encode

from rest_framework import serializers
from rest_framework.serializers import (
    PrimaryKeyRelatedField,
    ModelSerializer,
    Serializer,
)
from rest_framework.viewsets import (
    ModelViewSet,
    ViewSet,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.contrib.auth import login, logout

from logack_api.qrencode import qrencode
from logack_db.models import (
    Sub,
    Event,
    AuthToken,
)


class QrEncodedField(serializers.Field):
    """QrEncode"""
    def to_representation(self, value):
        """To Repr"""
        return b64encode(qrencode(value, "svg"))



class UserSerializer(ModelSerializer):
    """Serialize the user"""

    def to_representation(self, *args, **kwargs):
        """Add additonal fields to result"""
        rep = super().to_representation(*args, **kwargs)
        token = None;
        if not self.instance.is_anonymous:
            auth_token = self.instance.tokens.first()
            token = auth_token.token

        rep["token"] = token
        rep["token_qr"] = b64encode(qrencode(token, "svg"))

        return rep


    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name",
                  "is_anonymous"]


class UserCreateSerializer(ModelSerializer):
    """Create a new user"""
    class Meta:
        model = User
        fields = ["first_name"]


class UserViewSet(ViewSet):
    """Users"""
    def list(self, request):
        """Get the current user"""
        user = UserSerializer(request.user)
        return Response(user.data)

    def create(self, request):
        """Create a new user"""
        username = secrets.token_urlsafe(48)


        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User(
            username=username,
            **serializer.validated_data)
        user.save()

        token = AuthToken(user=user)
        token.save()

        serializer = UserSerializer(user)

        return Response(serializer.data)


class UserLoginSerializer(Serializer):
    """Login credentials"""
    token = serializers.CharField(max_length=96)


class LoginViewSet(ViewSet):
    """Login User"""
    def create(self, request):
        """Authenticate user"""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        token = AuthToken.objects.get(token=data["token"])
        login(request, token.user)

        serializer = UserSerializer(token.user)
        return Response(serializer.data)


class LogoutViewSet(ViewSet):
    """Logout User"""
    def list(self, request):
        """Close session"""
        logout(request)
        return Response({"ok": True})


class RelatedUserField(PrimaryKeyRelatedField):
    def get_queryset(self):
        """Get queryset"""
        qs = User.objects.all()
        request = self.context.get("request")
        if request:
            qs = User.objects.filter(id=request.user.id)

        return qs


class RelatedSubField(PrimaryKeyRelatedField):
    def get_queryset(self):
        """Get queryset"""
        qs = Sub.objects.all()
        request = self.context.get("request")
        if request:
            qs = Sub.objects.filter(user=request.user)

        return qs



class SubSerializer(ModelSerializer):
    """Sub serializer"""
    user = RelatedUserField()
    token_qr = QrEncodedField(source="token", read_only=True)

    class Meta:
        model = Sub
        fields = "__all__"
        read_only_fields = ["token", "token_qr"]


class SubViewSet(ModelViewSet):
    """Sub View"""
    serializer_class = SubSerializer
    permission_classes = [ IsAuthenticated ]

    def get_queryset(self):
        """Get the queryset"""
        return self.request.user.subs.all()


class EventSerializer(ModelSerializer):
    """Event serializer"""
    user = RelatedUserField()
    sub = RelatedSubField()

    class Meta:
        model = Event
        fields = "__all__"


class EventViewSet(ModelViewSet):
    """Event ViewSet"""
    serializer_class = EventSerializer
    permission_classes = [ IsAuthenticated ]

    def get_queryset(self):
        """Get the events in scope"""
        return self.request.user.events.all()


class LabelsViewSet(ViewSet):
    """Labels"""
    permission_classes = [ IsAuthenticated ]
    def list(self, request):
        """Get all labels for a user"""
        labels = request.user.events \
            .values_list("label", flat=True) \
            .distinct()

        return Response(labels)
