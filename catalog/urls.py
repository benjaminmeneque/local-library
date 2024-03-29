from django.urls import path

from catalog import views

urlpatterns = [
    path("", views.index, name="index"),
    path("books/", views.BookListView.as_view(), name="books"),
    path("book/<int:pk>", views.BookDetailView.as_view(), name="book-detail"),
    path("authors/", views.AuthorListView.as_view(), name="authors"),
    path("author/<int:pk>", views.AuthorDetailView.as_view(), name="author-detail"),
    path("mybooks/", views.LoanedBooksByUserListView.as_view(), name="my-borrowed"),
    path("borrowed/", views.LoanedBooksListView.as_view(), name="all-borrowed"),
    path(
        "book/<uuid:pk>/renew/", views.renew_book_librarian, name="renew-book-librarian"
    ),
    # author CUD
    path("author/create/", views.AuthorCreate.as_view(), name="author-create"),
    path("author/<int:pk>/update/", views.AuthorUpdate.as_view(), name="author-update"),
    path("author/<int:pk>/delete/", views.AuthorDelete.as_view(), name="author-delete"),
    # book CUD
    path("book/create/", views.BookCreate.as_view(), name="book-create"),
    path("book/<int:pk>/update/", views.BookUpdate.as_view(), name="book-update"),
    path("book/<int:pk>/delete/", views.BookDelete.as_view(), name="book-delete"),
    # signup
    path("signup/", views.SignUpView.as_view(), name="signup"),
    # language
    path(
        "language/create/", views.LanguageCreateView.as_view(), name="language-create"
    ),
    # genre
    path("genre/create/", views.GenreCreateView.as_view(), name="genre-create"),
    # bookinstance
    path(
        "bookinstance/create/",
        views.BookInstanceCreate.as_view(),
        name="book_instance-create",
    ),
    path(
        "bookinstance/<uuid:pk>/update/",
        views.BookInstance_for_user.as_view(),
        name="book_instance_update_for_user",
    ),
    path(
        "bookinstance/<uuid:pk>/staff/",
        views.BookInstance_for_staff.as_view(),
        name="book_instance_update_for_staff",
    ),
    # available books
    path("availablebooks/", views.available_book, name="available-books"),
    # search url
    path("search/", views.SearchResultListView.as_view(), name="search-results"),
]
