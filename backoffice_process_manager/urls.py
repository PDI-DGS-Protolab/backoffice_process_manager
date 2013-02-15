from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

import settings

urlpatterns = patterns('',

    url(r'^$', 'processes.views.index'),

    ######################################################
    # PAYMENT URLS
    ######################################################

    # payment data acquisition API
    url(r'^payment/acquire/service$',             'payment_gateways.views.acquire_service'),
    url(r'^payment/acquire/form/(?P<token>\w+)$', 'payment_gateways.views.acquire_form'),
    url(r'^payment/acquire/redirect$',            'payment_gateways.views.acquire_redirect'),

    # adyen callback API
    url(r'^payment/gw/adyen$', 'payment_gateways.adyen.callback.callback'),

    # worldpay callback API
    url(r'^payment/gw/worldpay/success$', 'payment_gateways.worldpay.callback.success'),
    url(r'^payment/gw/worldpay/pending$', 'payment_gateways.worldpay.callback.pending'),
    url(r'^payment/gw/worldpay/error$',   'payment_gateways.worldpay.callback.error'),

    ######################################################
    # PROCESSES
    ######################################################

    url(r'^processes/launchInvoicing/$',      'processes.views.launchInvoicing'),
    url(r'^processes/launchSyncInvoicing/$',  'processes.views.launchSyncInvoice'),

    url(r'^processes/chargingCallback/$',   'processes.views.chargingCallback'),

    url(r'^processes/getinfo/(?P<user_id>\w+)$', 'processes.views.get_processes'),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes':True}),
)
