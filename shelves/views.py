import os
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

import logging
logger = logging.getLogger(__name__)

from pathlib import Path

import mimetypes
# from django.conf import settings

from .forms import BooksAddViewForm, SearchBookForm
from .models import Reader, Books


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def process_search(request, kwargs):
    context = {'item_list': ""}
    id = request.user.id

    item_list = Books.search_query(id, kwargs)
    if item_list:
        context = {'item_list': item_list, 'list_head': 'matches'}
    else:
        context = {'item_list': '', 'list_head': 'matches'}
   
    return render(request, f'{BASE_DIR}/static/templates/list_draft.html', context) 


@login_required(login_url='users:login_user')
def book_search_view(request):
    if request.POST:
        form = SearchBookForm(request.POST)
        if form.is_valid():
            kwargs = form.cleaned_data
            return process_search(request, kwargs)
    else:
        return render(request, f'{BASE_DIR}/static/templates/query.html',
                      {'form': SearchBookForm()})


@login_required(login_url='users:login_user')
def table_books_view(request):
    list_head = 'table_books'
    id = request.user.id
    item_list = Books.objects.filter(reader_id=id)

    if request.method == 'POST':
        if request.POST.get('download', None):
            return download_file(request, item_list)

        for book in item_list:
            x = request.POST.get(str(book.id), 'off')
            # print(x)
            if x == 'on':
                book.delete()
        return redirect('shelves:table_books')
    else:
        return render(request, f'{BASE_DIR}/static/templates/list_draft.html', 
                    {'list_head': list_head, 'item_list': item_list})
    

@login_required(login_url='users:login_user')
def books_add_view(request):
    # print("request.user.id", request.user.id, request.user.username)
    logger.debug(f"user {request.user.id} {request.user.username}")

    if request.method == 'POST':
        author = request.POST['author']
        title = request.POST['title']
        tags = request.POST['tags']
        if not title and not author:
            ...
        else:
            obj, created = Reader.objects.get_or_create(
                            id=request.user.id, name=request.user.username)
            new_book = Books(title=title, author=author, tags=tags,
                        reader=obj)
            new_book.save()
            messages.success(request, 'book added')
            return redirect('shelves:books_add')

    return render(request, f'{BASE_DIR}/static/templates/books_add.html',
                  {'form': BooksAddViewForm()})


def download_file(request, item_list):
    filename = 'download.txt'
    dirname = BASE_DIR / f'static/download/'
    try:
        os.stat(dirname)
    except:
        os.mkdir(dirname)

    fl_path = dirname / f'{filename}'
    # fl_path = f'{BASE_DIR}/static/img/{filename}'
    # print(fl_path)
    with open(fl_path, 'w') as fl:
        for obj in item_list:
            line = " - ".join([obj.author, obj.title, obj.tags])
            fl.write(line)
            fl.write(";\n")

    with open(fl_path, 'rb') as fl:
        mime_type, _ = mimetypes.guess_type(fl_path)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = f"attachment; filename={filename}"
        return response
