# -*- coding: utf-8; -*-
from django.conf import settings


# обязательные параметры - реквизиты магазина
LOGIN = settings.QIWI_LOGIN
PASSWORD = settings.QIWI_PASSWORD

# lock timeout value. how long to wait for the lock to become available.
# default behavior is to never wait for the lock to be available.
LOCK_WAIT_TIMEOUT = getattr(settings, "QIWI_LOCK_WAIT_TIMEOUT", -1)
