# library/urls.py  

from django.urls import path, include  
from rest_framework.routers import DefaultRouter  
from .views import BookViewSet, TransactionViewSet , UserViewSet

router = DefaultRouter()  
router.register(r'books', BookViewSet)
router.register(r'users', UserViewSet)   

urlpatterns = [  
    path('', include(router.urls)),  
    path('transactions/<int:pk>/checkout/', TransactionViewSet.as_view({'post': 'checkout'}), name='checkout'),  
    path('transactions/<int:pk>/return/', TransactionViewSet.as_view({'post': 'return_book'}), name='return_book'),  
    path('transactions/', TransactionViewSet.as_view({'get': 'list'}), name='transaction-list'),  
]


# router = DefaultRouter()  
# router.register(r'users', UserViewSet)  
# router.register(r'books', BookViewSet)  
# router.register(r'transactions', TransactionViewSet, basename='transaction')  

# urlpatterns = [  
#     path('', include(router.urls)),  
# ] 

