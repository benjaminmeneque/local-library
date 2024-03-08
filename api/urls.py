from django.urls import include, path
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r"book", views.BookViewSet)
router.register(r"bookinstance", views.BookInstanceViewSet)
router.register(r"author", views.AuthorViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]

urlpatterns += router.urls
