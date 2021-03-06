#!/usr/bin/python
#coding=utf-8 

"""
Copyright 2012 Telefonica Investigación y Desarrollo, S.A.U

This file is part of Billing_PoC.

Billing_PoC is free software: you can redistribute it and/or modify it under the terms 
of the GNU Affero General Public License as published by the Free Software Foundation, either 
version 3 of the License, or (at your option) any later version.
Billing_PoC is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even 
the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero 
General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with Billing_PoC. 
If not, see http://www.gnu.org/licenses/.

For those usages not covered by the GNU Affero General Public License please contact with::mac@tid.es
""" 

'''
Created on 17/10/2012

@author: mac@tid.es
'''

from processes.payment_method_process   import PaymentMethodProcess
from payment_gateways.services          import PaymentGatewayManager
from payment_gateways.models            import PaymentMethod
from ordering.models                    import Order

from common.distributed.distributed import compute_uuid

from common.dates.dates import format_date

class PaymentGateway(object):

    def __init__(self, model):
        self.URL = model.endpoint

        self.USERNAME = model.merchant
        self.PASSWORD = model.password

        self.SUCCESS_CALLBACK = model.success_callback
        self.ERROR_CALLBACK = model.error_callback
        self.PENDING_CALLBACK = model.pending_callback

        self.MONEY    = 100
        self.CURRENCY = 'EUR'

        self.order = compute_uuid()

        self.gw = model
        
        self.gateways_manager         = PaymentGatewayManager()
        self.payment_method_process   = PaymentMethodProcess()

    def get_order(self):
        return self.order

    def get_gateway(self):
        return self.gw
    
    ###########################################################
    # Common data flows
    ########################################################### 
    
    def identify_successful_flow(self, order_code, mask, month, year, status):
        try:
            payment_method = PaymentMethod.objects.get(recurrent_order_code=order_code, status='PENDING')
        except PaymentMethod.DoesNotExist:
            payment_method = None

        # Distinguising flows
        if payment_method:
            return self._data_acquisition_flow(payment_method, mask, month, year, status)

        # Callback of recurrent payment flow
        try:
            order = Order.objects.get(order_code=order_code, status='PENDING')
        except Order.DoesNotExist:
            order = None

        if order:
            return self._recurrent_payment_flow(order, status)

        # Neither data acquistion flow nor recurrent payment flow, this is an error!
        print "ERROR: NEITHER ACQUISITION NOR RECURRENT FLOW IN ADYEN CALLBACK"
        return False
    
    def _data_acquisition_flow(self, payment_method, mask, month, year, status):
        # Callback of payment data acquisition flow
        print "DATA ACQUISITION FLOW"
        print status

        payment_method.mask  = mask
        payment_method.month = month
        payment_method.year  = year

        payment_method.status = status
        payment_method.save()

        fn = self.payment_method_process._start_standalone_new_payment_method_process

        # Start Async notify process
        self.payment_method_process.start_new_payment_method_notification_process(payment_method, fn)
    
    def _recurrent_payment_flow(self, order, status):
        # Callback of recuerrent payment flow
        print "RECURRENT ORDER FLOW"

        order.status = status
        order.save()
 
    ###########################################################
    # Should be overwritten by specific implementations of Payment Gateways
    ########################################################### 

    # account: customers.models.BillingAddress
    def get_redirect_url(self, billing_address):
        pass

    # order: customers.models.Order
    # payment_method: payment_gateways.models.PaymentMethod
    def recurrent_payment(self, order, payment_method):
        pass

    # data: dict. Data from the callback from the Payment Gateway
    def update_order_status(self, data):
        pass
