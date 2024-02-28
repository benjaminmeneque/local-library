import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from catalog.models import Author, BookInstance


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        help_text="Enter a date between now and 4 weeks (default 3).",
        widget=forms.DateInput(format="%m-%d-%Y", attrs={"type": "date"}),
    )

    def clean_renewal_date(self):
        data = self.cleaned_data["renewal_date"]

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(
                _("Invalid date - renewal in past"), code="invalid renewal date"
            )
        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _("Invalid date - renewal more than 4 weeks ahead"),
                code="invalid date range",
            )

        return data


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["first_name", "last_name", "date_of_birth", "date_of_death"]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "date_of_death": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_date_of_death(self):
        clean_date_of_death = self.cleaned_data.get("date_of_death")
        clean_date_of_birth = self.cleaned_data.get("date_of_birth")

        if clean_date_of_death and clean_date_of_birth:
            if clean_date_of_death < clean_date_of_birth:
                raise ValidationError(
                    _(
                        "Invalid date of death - the date of death is earlier than the date of birth."
                    )
                )

        return clean_date_of_death


class BookInstanceForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ["book", "imprint", "due_back", "borrower", "status"]
        widgets = {
            "due_back": forms.DateInput(attrs={"type": "date"}),
        }


class BookInstanceUpdateForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ["due_back", "borrower", "status"]
        widgets = {
            "due_back": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_due_back(self):
        clean_due_back = self.cleaned_data.get("due_back")

        if clean_due_back:
            if clean_due_back > datetime.date.today() + datetime.timedelta(weeks=4):
                raise ValidationError(
                    _("Invalid date - due back more than 4 weeks ahead")
                )

        return clean_due_back
