from django.test import TestCase, Client
from django import urls
import pytest
from django.contrib.messages import get_messages

import logging
logger = logging.getLogger(__name__)


from .views import *
from .models import UsersManageModel
from shelves.models import FirstReaderCreation, Books, Reader



@pytest.fixture()
def auto_login_user(db, client):
    user = UsersManageModel.objects.create(username="user1", password="qwerty12542")
    client.force_login(user)
    yield client, user
  
   

@pytest.mark.django_db
def test_user(auto_login_user):
    client, user = auto_login_user
    count = UsersManageModel.objects.all().count()
    assert count == 1


@pytest.mark.django_db
def test_reader(auto_login_user):
    client, user = auto_login_user 
    FirstReaderCreation.create_reader(user.id, user.username)
    count = Reader.objects.all().count()
    assert count == 1
    count = Books.objects.all().count()
    assert count == 2


@pytest.mark.django_db
def test_books_add_url(auto_login_user):
    client, user = auto_login_user
    response = client.get('/shelves/books_add/')
    assert response.status_code == 200
    assert b'add books' in response.content

    FirstReaderCreation.create_reader(user.id, user.username)
    book = Books(reader_id = user.id, author="AA", title="BB")
    book.save()
    count = Books.objects.all().count()
    assert count == 3

    # logger.debug(str(response.content))

    payload = dict(author = "ABC",
                        title = "adfg",
                        tags = ""
                    )
    response = client.post('/shelves/books_add/', payload)
    # assert response.status_code == 302
    count = Books.objects.all().count()
    assert count == 4




@pytest.mark.django_db
@pytest.mark.parametrize(
   'author, title, status_code', [
       ("", 'only_title', 400),
       ('only_author', "", 400),
       ('', '', 400),
       ('both', 'both', 200),
   ]
)
def test_books_add(
    author, title, status_code, 
    auto_login_user
     ):

    data = {
       'author': author,
       'title': title,
       'tags': ""
    }
    
    client, user = auto_login_user
    FirstReaderCreation.create_reader(user.id, user.username)
    response = client.post('/shelves/books_add/', data=data, follow=True)
    if status_code == 400: list(get_messages(response.wsgi_request)) == []
    if status_code == 200: 
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) >= 1
        assert str(messages[0]) == 'book added'


@pytest.fixture
def api_client():
   from rest_framework.test import APIClient
   return APIClient()


@pytest.mark.parametrize(
   'param', [
      '/shelves/books_add/',
      '/shelves/table_books/'
   ]
)
def test_unauthorized_request(param, api_client):
   response = api_client.get(param, follow=True)
   assert b"login" in response.content
   



@pytest.mark.django_db
def test_books_list(auto_login_user):
    client, user = auto_login_user
    FirstReaderCreation.create_reader(user.id, user.username)
    response = client.get('/shelves/table_books/')
    assert response.status_code == 200
    assert b'table of books' in response.content
    assert b'example_author_' in response.content

# 
# assertTemplateUsed(response, 'list_draft.html')
    






    




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

    
#     book = Books(reader_id = user.id, author="AA", title="BB")
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


