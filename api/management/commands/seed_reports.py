from django.core.management.base import BaseCommand

from api.models import Report


class Command(BaseCommand):
    help = "テスト用Reportデータを登録します"

    def handle(self, *args, **options):

        if Report.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    "Reportデータは既に存在します。追加登録しません。"
                )
            )
            return

        Report.objects.create(
            date="2026-10-01",
            address="千葉県印西市",
            title="テスト点検報告",
            status="完了",
        )

        self.stdout.write(
            self.style.SUCCESS(
                "テスト用Reportを1件登録しました。"
            )
        )