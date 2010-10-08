import logging
import time
from datetime import timedelta

import suds
from django.core.management.base import NoArgsCommand

from qiwi.conf import LOCK_WAIT_TIMEOUT, LOGIN, PASSWORD
from qiwi.lockfile import FileLock
from qiwi.models import Bill


logger = logging.getLogger(__name__)

class Command(NoArgsCommand):
    help = "Send SOAP requests createBill() to Qiwi."

    def handle_noargs(self, **options):
        lock = FileLock("qiwi_createbills")
        logger.debug("acquiring lock...")
        try:
            lock.acquire(LOCK_WAIT_TIMEOUT)
        except AlreadyLocked:
            logger.debug("lock already in place. quitting.")
            return
        except LockTimeout:
            logger.debug("waiting for the lock timed out. quitting.")
            return
        logger.debug("acquired.")
        
        start_time = time.time()
        success = 0
        fail = 0
        try:
            bills = Bill.objects.filter(soap_code=None)
            if bills.count() > 0:
                client = suds.client.Client('https://ishop.qiwi.ru/services/ishop?WSDL')
                for bill in bills:
                    code = client.service.createBill(
                        LOGIN,
                        PASSWORD,
                        bill.phone,
                        bill.amount,
                        'Zvooq payment for: %s' % bill.user.username,
                        bill.payment_no,
                        (bill.created_on + timedelta(days=7)).strftime('%d.%m.%Y %H:%M:%S'),
                        0,
                        False)
     
                    if code == 0:
                        success += 1
                        log = logger.debug
                    else:
                        fail += 1
                        log = logger.warning
     
                    log("createBill(phone: %s) = %d", bill.phone, code)
                    bill.soap_code = code
                    bill.save()

        finally:
            logger.debug("releasing lock...")
            lock.release()
            logger.debug("released.")
        
        logger.info("")
        logger.info("%s success; %s fail;", success, fail)
        logger.info("done in %.2f seconds", time.time() - start_time)
