from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BorrowingTransactionViewSet, ReservationViewSet

router = DefaultRouter()
router.register(r'borrowingtransactions', BorrowingTransactionViewSet, basename='borrowingtransaction')
router.register(r'reservations', ReservationViewSet, basename='reservation')

urlpatterns = [
    path('', include(router.urls)),
]
