from django import forms
from .models import Reader, Books


class SearchBookForm(forms.ModelForm):
    author = forms.CharField(label="author", max_length=200, 
            required=False,
                widget=forms.TextInput(attrs={
                    "placeholder": "author"
                }))
    title = forms.CharField(label="title", max_length=200,
            required=False,
                    widget=forms.TextInput(attrs={
                        "placeholder": "title"
                    }))
    tags = forms.CharField(label="tags", max_length=200, 
            required=False,
                widget=forms.TextInput(attrs={
                    "placeholder": "tags, separated by comma"
                }))
    class Meta:
        model = Books
        fields = [
            'author',
            'title',
            'tags'
        ]    


class BooksAddViewForm(forms.Form):
    author = forms.CharField(label="author", max_length=200)
    title = forms.CharField(label="title", max_length=200)
    tags = forms.CharField(label="tags", max_length=200, required=False)
