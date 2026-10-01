from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


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