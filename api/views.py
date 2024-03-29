from rest_framework import viewsets
from rest_framework.permissions import DjangoObjectPermissions, IsAdminUser

from api.serializers import AuthorSerializer, BookInstanceSerializer, BookSerializer
from catalog.models import Author, Book, BookInstance


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminUser]
    throttle_scope = "basic"


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]
    throttle_scope = "basic"
    filterset_fields = ["genre"]


class BookInstanceViewSet(viewsets.ModelViewSet):
    queryset = BookInstance.objects.all()
    serializer_class = BookInstanceSerializer
    permission_classes = [DjangoObjectPermissions]
    throttle_scope = "premium"
