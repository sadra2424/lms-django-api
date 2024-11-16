from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import BorrowerViewSet, CustomTokenObtainPairView

# ایجاد روتر و ثبت ViewSet
router = DefaultRouter()
router.register(r'borrowers', BorrowerViewSet, basename='borrower')

# تعریف urlpatterns
urlpatterns = [
    path('', include(router.urls)),  # شامل کردن مسیرهای ثبت شده در روتر
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
