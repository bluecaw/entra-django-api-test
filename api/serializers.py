from rest_framework import serializers

from api.models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            "id",
            "date",
            "address",
            "title",
            "status",
            "created_at",
            "updated_at",
        ]