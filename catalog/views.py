import datetime
from multiprocessing import context

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from catalog.forms import (
    AuthorForm,
    BookInstanceForm,
    BookInstanceUpdateForm_for_staff,
    BookInstanceUpdateForm_for_user,
    RenewBookForm,
)
from catalog.models import Author, Book, BookInstance, Genre, Language


# Create your views here.
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_genres = Genre.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact="a").count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "num_genres": num_genres,
        "num_visits": num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, "catalog/index.html", context=context)


def available_book(request):
    instances_available = BookInstance.objects.filter(status__exact="a")
    instances_reserve = BookInstance.objects.filter(status__exact="r")
    instances_maintenance = BookInstance.objects.filter(status__exact="m")

    instances_combined = instances_available | instances_reserve | instances_maintenance

    # Number of items per page
    items_per_page = 10  # You can change this value as per your requirement

    paginator = Paginator(instances_combined, items_per_page)
    page_number = request.GET.get("page")

    try:
        instances_paginated = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        instances_paginated = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        instances_paginated = paginator.page(paginator.num_pages)

    context = {
        "available_books": instances_available,
        "reserve_books": instances_reserve,
        "maintenance_books": instances_maintenance,
        "instances_paginated": instances_paginated,
    }

    return render(request, "catalog/available_book.html", context=context)


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class LanguageCreateView(PermissionRequiredMixin, CreateView):
    model = Language
    fields = ["name"]
    permission_required = "catalog.add_language"
    success_url = reverse_lazy("language-create")


class GenreCreateView(PermissionRequiredMixin, CreateView):
    model = Genre
    fields = ["name"]
    permission_required = "catalog.add_genre"
    success_url = reverse_lazy("genre-create")


class BookListView(generic.ListView):
    model = Book
    context_object_name = "book_list"
    template_name = "catalog/book_list.html"
    paginate_by = 2


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    template_name = "catalog/book_detail.html"


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = "author_list"
    template_name = "catalog/author_list.html"
    paginate_by = 2


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author
    template_name = "catalog/author_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.get_object()
        context["book_instance_count"] = BookInstance.objects.filter(
            book__author=author
        ).count()
        return context


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""

    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact="o")
            .order_by("due_back")
        )


class LoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    permission_required = ("catalog.can_mark_returned",)

    model = BookInstance
    template_name = "catalog/bookinstance_borrowed_list.html"
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact="o").order_by("due_back")


@login_required
@permission_required("catalog.can_renew", raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == "POST":

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data["renewal_date"]
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse("all-borrowed"))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={"renewal_date": proposed_renewal_date})

    context = {
        "form": form,
        "book_instance": book_instance,
    }

    return render(request, "catalog/book_renew_librarian.html", context)


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    form_class = AuthorForm
    permission_required = "catalog.add_author"


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    form_class = AuthorForm
    permission_required = "catalog.change_author"


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy("authors")
    permission_required = "catalog.delete_author"

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("author-delete", kwargs={"pk": self.object.pk})
            )


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = ["title", "author", "summary", "isbn", "language", "genre", "cover"]
    permission_required = "catalog.add_book"


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ["title", "author", "summary", "isbn", "language", "genre", "cover"]
    permission_required = "catalog.change_book"


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy("books")
    permission_required = "catalog.delete_book"


class BookInstanceCreate(PermissionRequiredMixin, CreateView):
    model = BookInstance
    form_class = BookInstanceForm
    permission_required = "catalog.add_bookinstance"
    success_url = reverse_lazy("book_instance-create")


class BookInstance_for_user(LoginRequiredMixin, UpdateView):
    model = BookInstance
    form_class = BookInstanceUpdateForm_for_user
    success_url = reverse_lazy("available-books")

    def form_valid(self, form):
        form.instance.borrower = self.request.user
        form.instance.status = "o"
        return super().form_valid(form)


class BookInstance_for_staff(PermissionRequiredMixin, UpdateView):
    model = BookInstance
    permission_required = "catalog.change_bookinstance"
    form_class = BookInstanceUpdateForm_for_staff
    success_url = reverse_lazy("available-books")
