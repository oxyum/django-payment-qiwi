
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    help = "Send SOAP requests createBill() to Qiwi."

    def handle_noargs(self, **options):
        pass