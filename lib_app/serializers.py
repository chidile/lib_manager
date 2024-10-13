from rest_framework import serializers  
from .models import Book, Transaction, CustomUser 


class UserSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = CustomUser  
        fields = ['id', 'username', 'email', 'date_joined', 'is_active', 'role']  

class BookSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Book  
        fields = ['id', 'title', 'author', 'isbn', 'published_date', 'copies_available']  

class TransactionSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Transaction  
        fields = ['id', 'user', 'book', 'checkout_date', 'return_date']