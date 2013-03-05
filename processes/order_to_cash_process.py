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

from models import BusinessProcess, SubProcess

from customer.tasks      import get_customer_details_from_sf_task
from charging.tasks      import charge_user_task
from rating.tasks        import download_and_parse_sdr_task
from pdf.tasks           import generate_pdf_and_upload_task
from email.tasks         import send_email_task
from notifications.tasks import create_order_summary_task

class OrderToCashProcess:

    def __init__(self):
        pass

    def start_order_to_cash_process(self, bucket_key, tef_account):

        sub_process = self._generate_billing_subprocess(bucket_key, tef_account)

        sp_id = sub_process.id

        chain = download_and_parse_sdr_task.s(True, bucket_key, tef_account, sp_id) | get_customer_details_from_sf_task.s(sp_id) | generate_pdf_and_upload_task.s(sp_id) | send_email_task.s(sp_id) | charge_user_task.s(sp_id) | create_order_summary_task.s(sp_id)

        chain()

    def sync_order_to_cash(self, bucket_key, tef_account):

        sub_process = self._generate_billing_subprocess(bucket_key, tef_account)

        sp_id = sub_process.id

        success = download_and_parse_sdr_task(True, bucket_key, tef_account, sp_id)
        success = get_customer_details_from_sf_task(success, sp_id)
        success = generate_pdf_and_upload_task(success, sp_id)
        success = send_email_task(success, sp_id)
        success = charge_user_task(success, sp_id)

        return success

    def _generate_billing_subprocess(self, bucket_key, tef_account):

        process = BusinessProcess(tef_account=tef_account, name='ORDER TO CASH', initial_data=bucket_key)
        process.save()

        sub_process = SubProcess(process=process, name='BILLING')
        sub_process.save()

        return sub_process


