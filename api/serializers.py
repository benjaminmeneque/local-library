from rest_framework import serializers

from catalog.models import Author, Book, BookInstance


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "first_name", "last_name", "date_of_birth", "date_of_death"]


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "summary", "isbn", "language", "genre"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["language"] = instance.language.name
        data["genre"] = [genre.name for genre in instance.genre.all()]
        return data


class BookInstanceSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = BookInstance
        fields = ["id", "book", "imprint", "due_back", "borrower", "status"]
        read_only_fields = ["id"]

    def get_status(self, obj):
        return dict(BookInstance.LOAN_STATUS).get(obj.status)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["book"] = instance.book.title
        data["borrower"] = instance.borrower.username if instance.borrower else None
        return data
