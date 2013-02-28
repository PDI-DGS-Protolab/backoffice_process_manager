from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

import settings

from payment_gateways.views import PaymentController
from processes.views        import ProcessesController
from processes.tos          import ToSController

from payment_gateways.adyen.callback    import AdyenCallbackController
from payment_gateways.worldpay.callback import WorldpayCallbackController

urlpatterns = patterns('',

    # ROOT. Now redirecting to processes index
    url(r'^$', ProcessesController.index),

    ######################################################
    # PAYMENT URLS
    ######################################################

    # payment data acquisition API
    url(r'^payment/acquire/service$',             PaymentController.acquire_service),
    url(r'^payment/acquire/form/(?P<token>\w+)$', PaymentController.acquire_form),
    url(r'^payment/acquire/redirect$',            PaymentController.acquire_redirect),

    # adyen callback API
    url(r'^payment/gw/adyen$', AdyenCallbackController.callback),

    # worldpay callback API
    url(r'^payment/gw/worldpay/success$', WorldpayCallbackController.success),
    url(r'^payment/gw/worldpay/pending$', WorldpayCallbackController.pending),
    url(r'^payment/gw/worldpay/error$',   WorldpayCallbackController.error),

    ######################################################
    # PROCESSES
    ######################################################

    url(r'^processes/launch_invoicing/$',        ProcessesController.launch_invoicing),
    url(r'^processes/launch_sync_invoicing/$',   ProcessesController.launch_sync_invoice),
    url(r'^processes/getinfo/(?P<user_id>\w+)$', ProcessesController.get_processes),

    ######################################################
    # TERMS OF SERVICE
    ######################################################

    url(r'^tos/$', ToSController.show),

    ######################################################
    # STATIC CONTENT
    ######################################################

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes':True}),
)
