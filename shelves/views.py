from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse    # , HttpResponseRedirect
from django.shortcuts import render, redirect

import mimetypes

import logging
logger = logging.getLogger(__name__)

from .forms import BooksAddViewForm, SearchBookForm
from .models import Reader, Books
from .download import AttachFile

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = settings.BASE_DIR


@login_required(login_url='users:login_user')
def book_search_view(request):
    if request.POST:
        form = SearchBookForm(request.POST)
        if form.is_valid():
            kwargs = form.cleaned_data
            item_list = Books.search_query(request.user.id, kwargs)
            context = {'item_list': item_list, 'list_head': 'matches'}
            return render(request, 
                          BASE_DIR / 'static/templates/list_draft.html',
                          context) 
    else:
        return render(request, BASE_DIR / 'static/templates/query.html',
                      {'form': SearchBookForm()})


@login_required(login_url='users:login_user')
def table_books_view(request):
    id = request.user.id
    item_list = Books.objects.filter(reader_id=id)

    if request.method == 'POST':
        if request.POST.get('download', None):
            AF = AttachFile(item_list)
            resp_obj = AF.attach_file()
            
            return resp_obj
        else:
            for book in item_list:
                x = request.POST.get(str(book.id), 'off')
                if x == 'on':
                    book.delete()
        return redirect('shelves:table_books')
    else:
        context = {'item_list': item_list, 
                   'list_head': 'table of books'}
        return render(request, 
                      BASE_DIR / 'static/templates/list_draft.html', 
                      context)
    

@login_required(login_url='users:login_user')
def books_add_view(request):
    # print("request.user.id", request.user.id, request.user.username)
    logger.debug(f"books_add_view, user {request.user.id} {request.user.username}")

    if request.method == 'POST':
        author = request.POST['author']
        title = request.POST['title']
        tags = request.POST['tags']
        if not title and not author:
            ...
        else:
            reader_obj = Reader.objects.get(id=request.user.id)

            new_book = Books(title=title, author=author, tags=tags,
                        reader=reader_obj)
            new_book.save()
            messages.success(request, 'book added')
            return redirect('shelves:books_add')

    return render(request, 
                  BASE_DIR / 'static/templates/books_add.html',
                  {'form': BooksAddViewForm()})

