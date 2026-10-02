from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.models import Report
from api.serializers import ReportSerializer


class HealthView(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({
            "status": "ok",
            "message": "Django API is working"
        })


class AuthTestView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "status": "ok",
            "message": "Authentication OK",
            "user": str(request.user),
        })


class ReportListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        reports = Report.objects.all().order_by("-date", "-id")

        serializer = ReportSerializer(reports, many=True)

        return Response(serializer.data)

class CreateReportView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReportSerializer(data=request.data)

        if serializer.is_valid():
            report = serializer.save()

            return Response(
                ReportSerializer(report).data,
                status=201
            )

        return Response(
            serializer.errors,
            status=400
        )

class DeleteReportView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            report = Report.objects.get(pk=pk)
        except Report.DoesNotExist:
            return Response(
                {"error": "Report not found"},
                status=404
            )

        report.delete()

        return Response(
            {
                "status": "ok",
                "message": "Report deleted",
                "id": pk
            },
            status=200
        )