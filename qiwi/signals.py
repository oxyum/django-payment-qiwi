from django.dispatch import Signal

payment_accepted = Signal(providing_args=["payment"])
