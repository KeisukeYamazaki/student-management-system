from django.core.management.base import BaseCommand

from app_base import *
from registry.google import regular_registry_by_google
from registry.models import TimeLimit

logger = getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        limit = TimeLimit.objects.filter(id=1).first()
        if limit:
            if limit.limit_date >= today:
                logger.info('定期試験自動登録 開始')
                regular_registry_by_google(limit.sheet_name)
                logger.info('定期試験自動登録 終了')
