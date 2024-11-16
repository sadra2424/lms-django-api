from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Report

class ReportListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, report_type=None):
        if report_type:
            reports = Report.objects.filter(report_type=report_type).order_by('-created_at')
        else:
            reports = Report.objects.all().order_by('-created_at')

        data = [
            {
                "id": report.id,
                "report_type": report.get_report_type_display(),
                "data": report.data,
                "created_at": report.created_at,
            }
            for report in reports
        ]
        return Response(data)
