from django.db import models


class Report(models.Model):
    date = models.DateField()
    address = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="未対応")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title