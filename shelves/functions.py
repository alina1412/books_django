from django.contrib import messages
from .models import Reader, Books
from .download import AttachFile


def get_books_of_user(id):
    return Books.objects.filter(reader_id=id)


def get_context_from_search(request, form):
    kwargs = form.cleaned_data
    item_list = Books.search_query(request.user.id, kwargs)
    context = {'item_list': item_list, 'list_head': 'matches'}
    return context


def get_file_to_attach(item_list):
    AF = AttachFile(item_list)
    return AF.attach_file()


def delete_checked_books(request, is_delete, item_list):
    if is_delete is not None:
        for book in item_list:
            x = request.POST.get(str(book.id), 'off')
            if x == 'on':
                book.delete()


def save_new_book(request):
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
