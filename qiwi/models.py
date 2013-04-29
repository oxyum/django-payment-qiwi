from datetime import datetime, timedelta
from time import sleep

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, models, transaction

import signals

class Bill(models.Model):
    user       = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_on = models.DateTimeField(unique=True, editable=False)
    payment_no = models.PositiveIntegerField(unique=True, editable=False)

    phone      = models.CharField(max_length=10)
    amount     = models.DecimalField(decimal_places=2, max_digits=7)

    soap_code  = models.IntegerField(blank=True, null=True)

    status     = models.IntegerField(blank=True, null=True)

    @transaction.commit_manually
    def save(self, force_insert=False, force_update=False, using=None):
        sid = transaction.savepoint()
        if self.pk is None:
            i = 1
            while self.pk is None:

                if i > 10:
                    sleep(0.001)

                if i > 20:
                    # Protection from infinite loop
                    raise IntegrityError('Too many iterations while generating unique Bill number.')

                try:
                    self.created_on = datetime.utcnow()
                    self.created_on = self.created_on - timedelta(microseconds = self.created_on.microsecond % 100)

                    self.payment_no = (self.created_on.hour*3600+
                                       self.created_on.minute*60+
                                       self.created_on.second)*10000 + (self.created_on.microsecond // 100)
                    super(Bill, self).save(force_insert, force_update)

                except IntegrityError:
                    transaction.savepoint_rollback(sid)

                i += 1
        else:
            super(Bill, self).save(force_insert, force_update)

        transaction.savepoint_commit(sid)
        transaction.commit()

    def __unicode__(self):
        return "%s - %s (%s)" % (self.payment_no, self.amount, self.phone)
