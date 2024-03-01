from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api import views

router = routers.DefaultRouter()
router.register(r"book", views.BookViewSet)
router.register(r"bookinstance", views.BookInstanceViewSet)
router.register(r"author", views.AuthorViewSet)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns += router.urls
