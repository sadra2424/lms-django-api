from django.urls import path
from .views import ReportListView

urlpatterns = [
    path('reports/', ReportListView.as_view(), name='reports-list'),
    path('reports/<str:report_type>/', ReportListView.as_view(), name='reports-detail'),
]
