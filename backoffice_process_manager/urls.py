from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

import settings

from payment_gateways.views import PaymentMethodController, ContractController, OrderingController
from processes.views        import ProcessesController
from processes.tos          import ToSController

from payment_gateways.adyen.callback    import AdyenCallbackController
from payment_gateways.worldpay.callback import WorldpayCallbackController

urlpatterns = patterns('',

    # ROOT. Now redirecting to processes index
    url(r'^$', ProcessesController.index),

    ######################################################
    # CONTRACT URLS
    ######################################################

    # contract management API
    url(r'^contract/new$', ContractController.create),

    ######################################################
    # PAYMENT METHOD URLS
    ######################################################

    # payment method acquisition API
    url(r'^account/(?P<account>\w+)/payment_method$',     PaymentMethodController.list),
    url(r'^account/(?P<account>\w+)/payment_method/new$', PaymentMethodController.create),

    # adyen callback API
    url(r'^payment_method/gw/adyen$', AdyenCallbackController.callback),

    # worldpay callback API
    url(r'^payment_method/gw/worldpay/success$', WorldpayCallbackController.success),
    url(r'^payment_method/gw/worldpay/pending$', WorldpayCallbackController.pending),
    url(r'^payment_method/gw/worldpay/error$',   WorldpayCallbackController.error),

    ######################################################
    # ORDERING
    ######################################################

    # ordering API
    url(r'^account/(?P<account>\w+)/order/new$', OrderingController.create),


    ######################################################
    # PROCESSES
    ######################################################

    url(r'^processes/launch_provision$',         ProcessesController.launch_provision),
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
