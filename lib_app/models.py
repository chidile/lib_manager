from django.db import models  
from django.contrib.auth.models import User  
from django.contrib.auth.models import AbstractUser  
from django.utils import timezone  
from datetime import timedelta 


class Book(models.Model):  
    title = models.CharField(max_length=255)  
    author = models.CharField(max_length=255)  
    isbn = models.CharField(max_length=13, unique=True)  
    published_date = models.DateField()  
    copies_available = models.PositiveIntegerField()  

    def __str__(self):  
        return f"{self.title} by {self.author}"  
        


class CustomUser(AbstractUser):  
    USER_ROLE_CHOICES = (  
        ('admin', 'Admin'),  
        ('member', 'Member'),  
    )  
    role = models.CharField(max_length=6, choices=USER_ROLE_CHOICES, default='member')  
    
    class Meta:
        ordering = ['-id']
        
    def __str__(self):  
        return self.username
    
    


class Transaction(models.Model):  
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  
    checkout_date = models.DateTimeField(auto_now_add=True)  
    return_date = models.DateTimeField(null=True, blank=True)  

    @property  
    def due_date(self):  
        return self.checkout_date + timedelta(days=14)  # 14 days to return  

    @property  
    def is_overdue(self):  
        return self.return_date is None and timezone.now() > self.due_date  

    @property  
    def penalty_due(self):  
        if self.is_overdue:  
            overdue_days = (timezone.now() - self.due_date).days  
            return overdue_days * 1.0  # Assuming $1 per overdue day  
        return 0.0
    
    def __str__(self):  
        return f"{self.book.title} by {self.user.username}"  