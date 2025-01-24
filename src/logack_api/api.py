import secrets

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

from logack_db.models import (
    Sub,
    Event,
)


class UserSerializer(ModelSerializer):
    """Serialize the user"""
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "is_anonymous"]


class UserCreateSerializer(ModelSerializer):
    """Create a new user"""
    class Meta:
        model = User
        fields = ["first_name"]


class UserLoginSerializer(Serializer):
    """Login credentials"""
    username = serializers.CharField(max_length=150)


class UserViewSet(ViewSet):
    """Users"""
    def list(self, request):
        """Get the current user"""
        user = UserSerializer(request.user)
        return Response(user.data)

    def create(self, request):
        """Create a new user"""
        username = secrets.token_urlsafe(48)
        token = secrets.token_urlsafe(64)

        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = User(
            username=username,
            last_name=token,
            first_name=data["first_name"])

        user.save()

        serializer = UserSerializer(user)

        return Response(serializer.data)


class LoginViewSet(ViewSet):
    """Login User"""
    def create(self, request):
        """Authenticate user"""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = User.objects.get(username=data["username"])
        login(request, user)

        serializer = UserSerializer(user)

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

    class Meta:
        model = Sub
        fields = "__all__"
        read_only_fields = ["token"]


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
