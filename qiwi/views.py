import logging

from hashlib import md5

from soaplib.serializers.primitive import Integer, String
from soaplib.service import DefinitionBase, rpc, TypeInfo, Message, MethodDescriptor
from soaplib.wsgi import Application

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from qiwi.conf import LOGIN, PASSWORD, TEST_MODE
from qiwi.models import Bill
from qiwi.signals import payment_accepted

logger = logging.getLogger(__name__)

# the class with actual web methods
class QiwiSOAPService(DefinitionBase):
    @rpc(String, String, String, Integer, _returns=Integer)
    def updateBill(self, login, password, txn, status):

        if login != LOGIN:
            logger.warning('Invalid login: %s, must be: %s', login, LOGIN)
            return 150

        gen_password = md5(''.join([txn, md5(PASSWORD).hexdigest().upper()])).hexdigest().upper()
        if not TEST_MODE and password != gen_password:
            logger.warning('Invalid password')
            return 150

        logger.info('Qiwi updateBill request: status %s for tx %s', status, txn)

        try:
            bill = Bill.objects.get(payment_no=txn)
        except Bill.DoesNotExist:
            return 210

        if bill.status is not None:
            return 215

        bill.status = status
        bill.save()

        if bill.status == 60:
            payment_accepted.send(sender=bill.__class__, payment=bill)

        return 0

# the class which acts as a wrapper between soaplib WSGI functionality and Django
class QiwiSoapApp(Application):
    def __call__(self, request):
        # wrap the soaplib response into a Django response object
        django_response = HttpResponse()
        def start_response(status, headers):
            status, reason = status.split(' ', 1)
            django_response.status_code = int(status)
            for header, value in headers:
                django_response[header] = value
        response = super(QiwiSoapApp, self).__call__(request.META, start_response)
        content = '\n'.join(response)

        # MAGIC BEGIN, DO NOT TOUCH! :(
        django_response.content = content.replace('s0:updateBillResult', 'updateBillResult')
        if django_response.has_header('Content-Length'):
            django_response['Content-Length'] = len(django_response.content)
        # MAGIC END

        return django_response

soap = csrf_exempt(QiwiSoapApp([QiwiSOAPService], 'http://client.ishop.mw.ru/'))
