from django.core.management.base import BaseCommand
from django.utils import timezone
from members.models import Member
from datetime import timedelta

class Command(BaseCommand):
    help = "Delete inactive members older than 24 hours"

    def handle(self, *args, **kwargs):
        threshold = timezone.now() - timedelta(hours=24)
        deleted_count, _ = Member.objects.filter(is_active=False, created_at__lt=threshold).delete()
        self.stdout.write(f"Deleted {deleted_count} inactive accounts.")
