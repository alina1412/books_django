import os
import mimetypes

import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse    # , HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from .forms import BooksAddViewForm, SearchBookForm
from .models import Reader, Books


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
            return download_file(request, item_list)
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
    logger.debug(f"user {request.user.id} {request.user.username}")

    if request.method == 'POST':
        author = request.POST['author']
        title = request.POST['title']
        tags = request.POST['tags']
        if not title and not author:
            ...
        else:
            reader_obj = Reader.objects.get(reader_id=request.user.id)

            new_book = Books(title=title, author=author, tags=tags,
                        reader=reader_obj)
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
        content_type = 'text/plain'
        # content_type, _ = mimetypes.guess_type(fl_path)
        # print(content_type)
        response = HttpResponse(fl, content_type=content_type)
        response['Content-Disposition'] = f"attachment; filename={filename}"
        return response
