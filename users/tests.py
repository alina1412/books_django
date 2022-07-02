from http import server
import imp
from lib2to3.pgen2 import driver
from lib2to3.pgen2.token import OP
from pathlib import WindowsPath
from pyexpat import model
from django.test import SimpleTestCase, TestCase, Client
from django import urls
import pytest
from django.contrib.messages import get_messages

# import logging
# logger = logging.getLogger(__name__)

from .views import *
from .models import UsersManageModel
from shelves.models import FirstReaderCreation, Books, Reader


# pytest-django has a build-in fixture client
@pytest.fixture()
def auto_login_user(db, client):
    print()
    print("fixture\n")
    user = UsersManageModel.objects.create(username="user1", password="qwerty12542")
    client.force_login(user)
    return client, user
    
   
# @pytest.mark.django_db
# def test_user(auto_login_user):
#     client, user = auto_login_user
#     count = UsersManageModel.objects.all().count()
#     assert count == 1

# @pytest.mark.parametrize(
#         'param', [
#             '/shelves/books_add/',
#             '/shelves/table_books/'
#         ]
#     )
# def test_unauthorized_request(param, client):
#    response = client.get(param, follow=True)
#    assert b"login" in response.content
   

# @pytest.mark.django_db
# def test_books_list(auto_login_user):
#     client, user = auto_login_user
#     FirstReaderCreation.create_reader(user.id, user.username)
#     response = client.get('/shelves/table_books/')
#     assert response.status_code == 200
#     assert b'table of books' in response.content
#     assert b'example_author_' in response.content



# @pytest.mark.parametrize(
#    'param, template_name', [
#       ('shelves:books_add', 'books_add.html'),
#       ('shelves:table_books', 'list_draft.html'),
#       ('shelves:book_search', 'query.html'),
#    ]
# )
# def test_registered_templates(param, template_name, client, auto_login_user):
#     client, user = auto_login_user
#     response = client.get(reverse(param))
#     assert response.templates
#     lst = list([t.name for t in response.templates])
#     print(lst)
#     lst = [x.__str__() if isinstance(x, WindowsPath) else x for x in lst]
#     assert [template_name in x for x in lst]


# @pytest.mark.parametrize(
#    'param, template_name', [
#       ('users:login_user', 'login_user.html'),
#       ('users:register', 'register.html'),
#    ]
# )
# def test_not_registered_templates(param, template_name, client):
#     # client, user = auto_login_user
#     response = client.get(reverse(param))
#     assert response.templates
#     lst = list([t.name for t in response.templates])
#     lst = [x.__str__() if isinstance(x, WindowsPath) else x for x in lst]
#     assert [template_name in x for x in lst]

    



    


#     # response = client.get('/shelves/table_books/')

#     FirstReaderCreation.create_reader(user.id, user.username)
#     book = Books(reader_id=user.id, author="AA", title="BB")
#     book.save()
#     book = Books(reader_id=user.id, author="CC", title="DD")
#     book.save()
#     count = Books.objects.all().count()
#     assert count == 4

#     payload = {'delete': True, 'request': 'delete'}
                    
#     response = client.post('/shelves/table_books/', payload)
#     # assert response.status_code == 200
#     print(response.content)
#     # assert response == "a"

#     count = Books.objects.all().count()
#     assert count == 4


# @pytest.fixture

# @pytest.mark.django_db
# def test_create_user():
#     UsersManageModel.objects.create(username="A", password="qwerty12542")
#     UsersManageModel.objects.create(username="B", password="qwerty12542")
#     count = UsersManageModel.objects.all().count()
#     print(count)
#     assert count == 2

# # @pytest.mark.parametrize('param', ['register'])
# def test_render_view(client):
#     # tmp_url = urls.reverse(param)
#     resp = client.get('/users/register/')
#     assert resp.status_code == 200


# @pytest.mark.django_db
# def test_count():
#     count = UsersManageModel.objects.all().count()
#     print(count)
#     assert count == 2




# @pytest.mark.django_db
# def test_with_authenticated_client(client, django_user_model):
#     username = "user1"
#     # password = "bar"
#     user = UsersManageModel.objects.create(username=username, password="qwerty12542")
#     # count = UsersManageModel.objects.all().count()
#     # assert count == 1
#     # Use this:
#     client.force_login(user)
#     # # Or this:
#     # client.login(username=username, password=password)
#     response = client.get('/shelves/books_add/')
#     assert response.status_code == 200

#     FirstReaderCreation.create_reader(user.id, username)
#     count = Reader.objects.all().count()
#     assert count == 1

    
#     book = Books(reader_id=user.id, author="AA", title="BB")
#     book.save()
#     count = Books.objects.all().count()
#     assert count == 3

#     payload = dict(author = "ABC",
#                     title = "adfg",
#                     tags = ""
#                    )
#     response = client.post('/shelves/books_add/', payload)
#     # assert response.status_code == 302
#     count = Books.objects.all().count()
#     assert count == 4
