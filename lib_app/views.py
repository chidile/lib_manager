from rest_framework import viewsets, status
from rest_framework.response import Response  
from rest_framework import filters 
from .models import Book, Transaction, CustomUser
from .serializers import BookSerializer, TransactionSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404  
from django.utils import timezone 
from datetime import timedelta  
from .util import send_email_notification
from django.contrib.auth.models import User 


class UserViewSet(viewsets.ModelViewSet):  
     
    queryset = CustomUser.objects.all()  
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser] 

class BookViewSet(viewsets.ModelViewSet):  
    
    queryset = Book.objects.all()  
    serializer_class = BookSerializer  
    filter_backends = [filters.OrderingFilter, filters.SearchFilter] 
    
    # Define the fields that can be searched   
    search_fields = ['title', 'author', 'isbn']  
    ordering_fields = ['title', 'author', 'published_date']  
    permission_classes = [IsAuthenticated] 

    def create(self, request, *args, **kwargs):  
        """  
        Create a new book instance.  
        """  
        serializer = self.get_serializer(data=request.data)  
        serializer.is_valid(raise_exception=True)  
        self.perform_create(serializer)  
        return Response(serializer.data, status=status.HTTP_201_CREATED)  

class TransactionViewSet(viewsets.ViewSet):  
    """  
    A viewset for managing transactions (checkouts and returns).  
    """  
    permission_classes = [IsAuthenticated]  

    def notify_user(self, user, message):  
        subject = 'Library Notification'  
        send_email_notification(user.email, subject, message)  

    def checkout(self, request, pk=None):  
        """  
        Check out a book for the authenticated user.  
        """  
        book = get_object_or_404(Book, pk=pk)  
        if book.copies_available > 0:  
            transaction = Transaction.objects.create(user=request.user, book=book)  
            book.copies_available -= 1  
            book.save()  
            return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)  
        return Response({"detail": "No copies available."}, status=status.HTTP_400_BAD_REQUEST)  

    def return_book(self, request, pk=None):  
        """  
        Return a checked-out book for the authenticated user.  
        """  
        transaction = get_object_or_404(Transaction, pk=pk, user=request.user, return_date=None)  
        transaction.return_date = timezone.now()  

        if transaction.is_overdue:  
            overdue_days = (timezone.now() - transaction.due_date).days  
            penalty = overdue_days * 1.0  # Calculation for penalty  
            message = f"You have returned an overdue book. Your penalty is ${penalty}."  
        else:  
            message = "You have returned the book on time."  

        self.notify_user(transaction.user, message)  

        transaction.book.copies_available += 1  
        transaction.book.save()  
        transaction.save()  
        return Response({"detail": "Book returned successfully."}, status=status.HTTP_200_OK)  

    def list(self, request):  
        """  
        List all transactions for the authenticated user.  
        """  
        transactions = Transaction.objects.filter(user=request.user)  
        serializer = TransactionSerializer(transactions, many=True)  
        return Response(serializer.data)

    def list_overdue(self, request):  
        """  
        List all overdue transactions for the authenticated user.  
        """  
        transactions = Transaction.objects.filter(user=request.user, return_date=None, checkout_date__lt=timezone.now() - timedelta(days=14))  
        serializer = TransactionSerializer(transactions, many=True)  
        return Response(serializer.data)


# # library/views.py  

# from rest_framework import viewsets, permissions, status  
# from rest_framework.response import Response  
# from .models import CustomUser, Book, Transaction  
# from .serializers import UserSerializer, BookSerializer, TransactionSerializer  
# from django.shortcuts import get_object_or_404  
# from django.core.mail import send_mail  
# from django.conf import settings  

# class UserViewSet(viewsets.ModelViewSet):  
#     """  
#     A viewset for managing users (CRUD operations).  
#     Admin users can manage all users.  
#     """  
#     queryset = CustomUser.objects.all()  
#     serializer_class = UserSerializer  
#     permission_classes = [permissions.IsAdminUser]  # Only admins can manage users  

# class BookViewSet(viewsets.ModelViewSet):   
#     queryset = Book.objects.all()  
#     serializer_class = BookSerializer  
#     permission_classes = [permissions.IsAuthenticated]  

#     def get_queryset(self):  
#         # Filter books by availability if specified  
#         queryset = super().get_queryset()  
#         available = self.request.query_params.get('available', None)  
#         if available is not None:  
#             queryset = queryset.filter(copies_available__gt=0)  
#         return queryset  

# class TransactionViewSet(viewsets.ViewSet):  
#     """  
#     A viewset for managing book transactions (check-out and return).  
#     Users can check out and return books.  
#     """  
#     permission_classes = [permissions.IsAuthenticated]  

#     def checkout(self, request, pk=None):  
#         book = get_object_or_404(Book, pk=pk)  
#         user = request.user  

#         # Check if the user already has a book checked out  
#         if Transaction.objects.filter(user=user, return_date=None).exists():  
#             return Response({"detail": "You can only check out one book at a time."}, status=status.HTTP_400_BAD_REQUEST)  

#         # Check if the book has available copies  
#         if book.copies_available <= 0:  
#             return Response({"detail": "No available copies."}, status=status.HTTP_400_BAD_REQUEST)  

#         # Create a new transaction  
#         transaction = Transaction.objects.create(user=user, book=book)  
#         book.copies_available -= 1  
#         book.save()  

#         return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)  

#     def return_book(self, request, pk=None):  
#         transaction = get_object_or_404(Transaction, pk=pk, user=request.user, return_date=None)  
#         transaction.return_date = timezone.now()  
#         transaction.book.copies_available += 1  
#         transaction.book.save()  
#         transaction.save()  

#         # Notify user about the return  
#         if transaction.is_overdue:  
#             penalty = transaction.penalty_due  
#             message = f"You have returned an overdue book. Your penalty is ${penalty}."  
#         else:  
#             message = "You have returned the book on time."  

#         self.notify_user(transaction.user.email, message)  

#         return Response({"detail": "Book returned successfully."}, status=status.HTTP_200_OK)  

#     def notify_user(self, user_email, message):  
#         subject = 'Library Notification'  
#         send_mail(  
#             subject,  
#             message,  
#             settings.EMAIL_HOST_USER,  
#             [user_email],  
#             fail_silently=False,  
#         )