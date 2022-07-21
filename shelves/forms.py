from django import forms
from .models import Books


class SearchBookForm(forms.ModelForm):
    author = forms.CharField(label="author", max_length=200,
                             required=False,
                             widget=forms.TextInput(attrs={"class": "form_field",
                                                           "placeholder": "author",
                                                           'autofocus': True}))

    title = forms.CharField(label="title", max_length=200,
                            required=False,
                            widget=forms.TextInput(attrs={"class": "form_field",
                                                          "placeholder": "title"}))

    tags = forms.CharField(label="tags", max_length=200,
                           required=False,
                           widget=forms.TextInput(attrs={"class": "form_field",
                                                         "placeholder": "tags, separated by comma"}))

    class Meta:
        model = Books
        fields = [
            'author',
            'title',
            'tags'
        ]


class BooksAddViewForm(forms.Form):
    author = forms.CharField(label="author", max_length=200,
                             widget=forms.TextInput(attrs={"class": "form_field",
                                                           "placeholder": "author",
                                                           'autofocus': True}))

    title = forms.CharField(label="title", max_length=200,
                            widget=forms.TextInput(attrs={"class": "form_field",
                                                          "placeholder": "title"}))

    tags = forms.CharField(label="tags", max_length=200, required=False,
                           widget=forms.TextInput(attrs={"class": "form_field",
                                                         "placeholder": "tags, separated by comma"}))
