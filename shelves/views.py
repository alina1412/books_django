from django.conf import settings
# from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse    # , HttpResponseRedirect
from django.shortcuts import render, redirect

import logging
logger = logging.getLogger(__name__)


from shelves.functions import delete_checked_books,\
                                get_books_of_user,\
                                get_context_from_search,\
                                get_file_to_attach,\
                                save_new_book

from .forms import BooksAddViewForm, SearchBookForm

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = settings.BASE_DIR


@login_required(login_url='users:login_user')
def book_search_view(request):
    if request.POST:
        form = SearchBookForm(request.POST)
        if form.is_valid():
            context = get_context_from_search(request, form)
            return render(request, 
                          BASE_DIR / 'static/templates/list_draft.html',
                          context) 
    return render(request,
                  BASE_DIR / 'static/templates/query.html',
                  {'form': SearchBookForm()})


@login_required(login_url='users:login_user')
def table_books_view(request):
    item_list = get_books_of_user(request.user.id)

    if request.method == 'POST':
        is_download_query = request.POST.get('download', None)
        if is_download_query is not None:
            resp_obj = get_file_to_attach(item_list)
            return resp_obj
        is_delete = request.POST.get('delete', None)
        delete_checked_books(request, is_delete, item_list)
        return redirect('shelves:table_books')
    context = {'item_list': item_list, 'list_head': 'table of books'}
    return render(request, 
                  BASE_DIR / 'static/templates/list_draft.html', 
                  context)
    

@login_required(login_url='users:login_user')
def books_add_view(request):
    # logger.debug(f"books_add_view, user {request.user.id} {request.user.username}")
    if request.method == 'POST':
        save_new_book(request)
        return redirect('shelves:books_add')

    return render(request, 
                  BASE_DIR / 'static/templates/books_add.html',
                  {'form': BooksAddViewForm()})
