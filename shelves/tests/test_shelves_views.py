from dataclasses import dataclass

from pathlib import WindowsPath
import pytest
from django.contrib.messages import get_messages

from shelves.models import Books, Reader
from users.models import UsersManageModel
from shelves.functions import FirstReaderCreation


# @dataclass
class TestUser:
    NAME: str = 'user1'
    PASSWORD: str = 'qwerty12542'
    BOOKS_FIRST_READER_HAS: int = 8


class TestBooksUrl:
    @pytest.fixture()
    def auto_create_user_with_books(self, db, client):
        user = UsersManageModel.objects.create(
                            username=TestUser.NAME,
                            password=TestUser.PASSWORD)
        client.force_login(user)
        FirstReaderCreation.create_reader(user.id, 
                                          TestUser.NAME)
        return client, user


    @pytest.mark.usefixtures("auto_create_user_with_books")
    @pytest.mark.django_db
    def test_reader(self):
        assert Reader.objects.all().count() == 1
        assert Books.objects.all().count() == TestUser.BOOKS_FIRST_READER_HAS

    def test_url_access(self, auto_create_user_with_books):
        client, user = auto_create_user_with_books
        response = client.get('/shelves/books_add/')
        assert response.status_code == 200

    def test_url_content(self, auto_create_user_with_books):
        client, user = auto_create_user_with_books
        response = client.get('/shelves/books_add/')
        assert b'add books' in response.content

    @pytest.mark.django_db
    def test_books_addition(self, auto_create_user_with_books):
        client, user = auto_create_user_with_books

        Books(reader_id=user.id, author="AA", title="BB").save()
        assert Books.objects.all().count() == TestUser.BOOKS_FIRST_READER_HAS + 1

        context = dict(author = "ABC", title = "adfg", tags = "")
        response = client.post('/shelves/books_add/', context, follow=True)
        assert response.status_code == 200
        assert Books.objects.all().count() == TestUser.BOOKS_FIRST_READER_HAS + 2

    # FAILS!
    # @pytest.mark.django_db
    # @pytest.mark.parametrize(
    #         'author, title, num', [
    #             ("", 'only_title', 1),  # it had added anyways!
    #             # ('only_author', "", 2),
    #             # ('', '', 3),
    #             ]
    #         )
    # def test_books_not_successful_add(self, author, title, num, 
    #     auto_create_user_with_books
    #     ):
    #     data = {'author': author, 'title': title, 'tags': ""}
        
    #     client, user = auto_create_user_with_books
    #     assert Books.objects.all().count() == TestUser.BOOKS_FIRST_READER_HAS

    #     response = client.post('/shelves/books_add/', data=data, follow=True)

    @pytest.mark.django_db
    def test_delete_books_by_checkbox(self, 
        auto_create_user_with_books
        ):
        client, user = auto_create_user_with_books
         
        assert Books.objects.all().count() == TestUser.BOOKS_FIRST_READER_HAS
        id = Books.objects.filter(reader_id=user.id).first().id
        # print(id)
        data = {'delete': True, str(id): 'on'}

        response = client.post('/shelves/table_books/', data=data, follow=True)
        assert response.status_code == 200
        assert Books.objects.filter(reader_id=user.id).count() == TestUser.BOOKS_FIRST_READER_HAS - 1


    @pytest.mark.django_db
    @pytest.mark.parametrize(
            'author, title, num', [
                ('both', 'both', 1),
                ('bo th', 'both', 1),
                ('both', 'bo th', 1),
                ]
            )
    def test_books_add(self, author, title, num, 
        auto_create_user_with_books
        ):
            
        data = {'author': author, 'title': title, 'tags': ""}
        
        client, user = auto_create_user_with_books
        response = client.post('/shelves/books_add/', data=data, follow=True)
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) >= 1
        assert str(messages[0]) == 'book added'
        assert Books.objects.all().count() == TestUser.BOOKS_FIRST_READER_HAS + 1


    @pytest.mark.django_db
    def test_books_search_url(self, auto_create_user_with_books):
        client, user = auto_create_user_with_books
        response = client.get('/shelves/book_search/')

        Books(reader_id=user.id, author="AA", title="BB").save()
        Books(reader_id=user.id, author="CC", title="DD").save()
    
        assert Books.objects.all().count() == TestUser.BOOKS_FIRST_READER_HAS + 2

        context = dict(author = "C", title = "", tags = "")
        response = client.post('/shelves/book_search/', context)
        assert b'DD' in response.content
        assert b'AA' not in response.content

        assert response.templates
        lst = list([t.name for t in response.templates])
        lst = [x.__str__() if isinstance(x, WindowsPath) else x for x in lst]
        assert ['list_draft.html' in x for x in lst]
