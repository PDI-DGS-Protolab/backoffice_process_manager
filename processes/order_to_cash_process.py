#!/usr/bin/python
# coding=utf-8

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
Created on 05/02/2013

@author: mac@tid.es
'''

from common.aws.s3   import get_sdr_request_keys

from customer.tasks      import get_customer_details_from_sf_task
from charging.tasks      import charge_user_task
from rating.tasks        import download_and_parse_sdr_task, rate_from_order_task, create_order_task
from pdf.tasks           import generate_pdf_and_upload_task
from email.tasks         import send_invoice_email_task
from notifications.tasks import create_order_summary_on_salesforce_task

from customers.models import Account

from django.test.utils import override_settings

from process import Process

class OrderToCashProcess(Process):

    def start_order_to_cash(self):
        keys = get_sdr_request_keys()

        for key in keys:
            self.start_cdr_order_to_cash_process(key.name, self._get_account(key))

    ################################################################################
    # CREATE & START PROCESSES
    ################################################################################
    def start_cdr_order_to_cash_process(self, bucket_key, account):
        
        process    = self.create_process_model(account,    'ORDER TO CASH')
        subprocess = self.create_subprocess_model(process, 'BILLING')

        self._start_salesforce_cdr_order_to_cash_process(bucket_key, account, subprocess)

    def start_online_order_to_cash_process(self, order, line_items, account, billing_address):

        process    = self.create_process_model(account,    'ORDER TO CASH')
        subprocess = self.create_subprocess_model(process, 'BILLING')

        self._start_standalone_online_order_to_cash_process(order, line_items, billing_address, subprocess)
    
    ################################################################################
    # PRIVATE METHODS
    ################################################################################

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS = True, CELERY_ALWAYS_EAGER = True, BROKER_BACKEND = 'memory')
    def _start_salesforce_cdr_order_to_cash_process(self, bucket_key, account, subprocess):
        
        sp_id      = subprocess.id
        account_id = account.account_id
        
        chain = download_and_parse_sdr_task.s(True, bucket_key, account_id, sp_id) | get_customer_details_from_sf_task.s(sp_id) | create_order_task(sp_id) | generate_pdf_and_upload_task.s(sp_id) | send_email_task.s(sp_id) | charge_user_task.s(sp_id) | create_order_summary_on_salesforce_task.s(sp_id)

        chain()

    def _start_standalone_online_order_to_cash_process(self, order, line_items, billing_address, subprocess):

        sp_id = subprocess.id

        # Serializing data objects in order to remove no-serializable fields (database connections, etc)
        # Every argument passed to Celery tasks must be JSON serializable => python dict for example, objects are not Json serializable
        order_dict      = order.to_dict()
        line_items_dict = [line_item.to_dict() for line_item in line_items]
        billing_address_dict = billing_address.to_dict()

        chain = rate_from_order_task.s(True, order_dict, line_items_dict, billing_address_dict, sp_id) | generate_pdf_and_upload_task.s(sp_id) | send_invoice_email_task.s(sp_id) | charge_user_task.s(sp_id)

        chain()

        # return customers.model.Account
    def _get_account(self, key):
        # By convention, by removing the last 4 characters from key, the tef_account is returned!
        account_id = key.name[0:-4]

        try:
            return Account.objects.get(account_id=account_id)
        except Exception, e:
            print "Missing account: {0}".format(account_id)
            return None