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


lst = [
    {'author': 'Hans Christian Andersen',
     'title': 'The Ugly Duckling', 'tags': 'tale'},
    {'author': 'Jan Ormerod', 'title': 'The Frog Prince',
     'tags': 'tale'},
    {'author': 'Robert Southey',
     'title': 'Goldilocks and the Three Bears ', 'tags': 'tale'},
    {'author': 'Oscar Wilde', 'title': 'The Happy Prince',
     'tags': 'tale'},
    {'author': 'Michael Morpurgo', 'title': 'Hansel and Gretel',
     'tags': 'tale'},
    {'author': 'Daniel Kahneman',
     'title': 'Thinking, Fast and Slow', 'tags': 'education, science'},
    {'author': 'Yuval Noah Harari',
     'title': 'Sapiens: A Brief History of Humankind', 'tags': 'science'},
    {'author': 'Robert Sapolski',
     'title': 'Zapiski Primata', 'tags': 'science'}
]


class FirstReaderCreation:
    def create_reader(id, username):
        print('started to create reader...')
        reader_obj = Reader.objects.create(pk=id, name=username)
        FirstReaderCreation.create_example_books(reader_obj)
        print('created reader!')

    def create_example_books(reader_obj):
        # for i in range(2):
        # example_author = f"example_author_{i}"
        # example_title = f"example_title_{i}"
        # example_tags = "tag1, tag2"
        for item in lst:
            example_author = item['author']
            example_title = item['title']
            example_tags = item['tags']

            new_book = Books(author=example_author,
                             title=example_title,
                             tags=example_tags,
                             reader=reader_obj)
            new_book.save()
