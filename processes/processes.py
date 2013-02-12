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

from tasks import notify_salesforce_task, notify_tef_accounts_task, payment_gateway_invocation_task,\
                  download_and_parse_sdr_task, get_customer_details_from_sf_task, \
                  generate_pdf_and_upload_task, send_email_task, charge_user_task, update_charging_result, \
                  create_financial_accounting_record

from models import BusinessProcess, SubProcess

######################################################
# DATA ACQUISITION PROCESS
######################################################

def start_notify_data_acquisition_result(status, contact_id):
    chain = notify_salesforce_task.s(status, contact_id) | notify_tef_accounts_task.s(status, contact_id)

    chain()

def sync_notify_data_acquisition_result(status, contact_id):
    result = notify_salesforce_task(status, contact_id)
    result = notify_tef_accounts_task(status, contact_id)

    return result

######################################################
# RECURRENT PAYMENT PROCESSES
######################################################

def start_invoke_gateway(json, p_gw):
    chain = payment_gateway_invocation_task.s(json)

    chain()

def sync_invoke_gateway(json, p_gw):
    result = payment_gateway_invocation_task(json)

    return result

######################################################
# ORDER TO CASH PROCESS
######################################################

def start_order_to_cash_process(bucket_key, tef_account):

    sub_process =_generate_billing_subprocess(bucket_key, tef_account)

    sp_id = sub_process.id

    chain = download_and_parse_sdr_task.s(True, bucket_key, sp_id) | get_customer_details_from_sf_task.s(sp_id) | generate_pdf_and_upload_task.s(sp_id) | send_email_task.s(sp_id) | charge_user_task.s(sp_id)

    chain()

def sync_order_to_cash(bucket_key, tef_account):

    sub_process =_generate_billing_subprocess(bucket_key, tef_account)

    sp_id = sub_process.id

    success = download_and_parse_sdr_task(True, bucket_key, sp_id)
    success = get_customer_details_from_sf_task(success, sp_id)
    success = generate_pdf_and_upload_task(success, sp_id)
    success = send_email_task(success, sp_id)
    success = charge_user_task(success, sp_id)

    return success

######################################################
# COLLECTIONS PROCESS
######################################################

def start_collections_process(json):
    chain = update_charging_result.s(json) | create_financial_accounting_record.s()

    chain()

######################################################
# AUX FUNCTIONS
######################################################

def _generate_billing_subprocess(bucket_key, tef_account):
    process = BusinessProcess(tef_account=tef_account, name='ORDER TO CASH', initial_data=bucket_key)
    process.save()

    sub_process = SubProcess(process=process, name='BILLING')
    sub_process.save()

    return sub_process