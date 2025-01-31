from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from django.contrib.auth.models import User
from logack_db.models import (
    Sub,
)


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """Authenticate the request"""
        header = request.META.get("HTTP_AUTHORIZATION")
        if not header:
            return (None, None)

        (token_type, token) = header.split(" ", 2)
        if token_type != "Beerer":
            raise AuthenticationFailed("Invalid token type")

        # Lookup user or sub
        user = User.objects.filter(last_name=token).first()
        if user:
            return (user, token)
        
        sub = Sub.objects.filter(token=token).first()
        if sub:
            return (sub.user, token)

        return (None, None)

