from django.contrib import admin
from .models import Book, CustomUser, Transaction  


# Register your models here.
admin.site.register(Book)  
admin.site.register(CustomUser)  
admin.site.register(Transaction)