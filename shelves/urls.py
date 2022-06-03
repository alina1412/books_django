from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views


app_name = 'shelves'
urlpatterns = [
    path('books_add/', views.books_add_view, name='books_add'),
    path('table_books/', views.table_books_view, name='table_books'),
    path('book_search/', views.book_search_view, name='book_search'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
