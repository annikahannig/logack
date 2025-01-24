
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from logack_api import api

router = DefaultRouter()
router.register(r"user", api.UserViewSet,
                basename="user")
router.register(r"login", api.LoginViewSet,
                basename="auth-login")
router.register(r"logout", api.LogoutViewSet,
                basename="auth-logout")
router.register(r"subs", api.SubViewSet,
                basename="sub")
router.register(r"events", api.EventViewSet,
                basename="event")

urlpatterns = [
    path("", include(router.urls)),
]



