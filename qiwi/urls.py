
from django.conf.urls.defaults import *

urlpatterns = patterns('qiwi.views',
    url(r'^soap/$', 'soap', name='qiwi-soap'),
)
