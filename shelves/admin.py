from django.contrib import admin

from .models import Reader, Books


admin.site.register([Reader, Books])
