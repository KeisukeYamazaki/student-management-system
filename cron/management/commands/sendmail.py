from django.core.management import BaseCommand

from mail import send_log_mail


class Command(BaseCommand):
    def handle(self, *args, **options):
        send_log_mail()
