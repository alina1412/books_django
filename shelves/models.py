from django.db import models
from django.db.models import Q

class Reader(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Books(models.Model):
    reader = models.ForeignKey(
        Reader,
        on_delete=models.CASCADE,
    )
    author = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    tags = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['author']

    def search_query(id, kwargs): # -> item_list
        s1 = set(Books.objects.filter(
                Q(reader_id=id) & 
                Q(title__icontains=kwargs['title']))) if kwargs['title'] else set()
        s2 = set(Books.objects.filter(
                Q(reader_id=id) & 
                Q(author__icontains=kwargs['author']))) if kwargs['author'] else set()
        s3 = set(Books.objects.filter(
                Q(reader_id=id) & 
                Q(tags__icontains=kwargs['tags']))) if kwargs['tags'] else set()
        
        item_list = set() | s1 | s2 | s3
        return item_list

    class Meta:
        verbose_name_plural = "Books"

class FirstReaderCreation:

    def create_reader(id, username):
        print('started to create reader...')
        reader_obj = Reader.objects.create(pk=id, name=username)

        example_author = "example_author"
        example_title = "example_title"
        example_tags = "tag1, tag2"
        for _ in range(2):
            new_book = Books(author=example_author,
                            title=example_title, 
                            tags=example_tags,
                            reader=reader_obj)
            new_book.save()
        print('created reader!')
