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
Created on 15/10/2012

@author: mac@tid.es
'''

from celery import task

from common.salesforce.salesforce import update_contact, activate_contract, create_order_summary
from sdr_gen                      import generate_and_upload_sdr

from processes.task_manager import TaskManager

@task(ignore_result=True)
def notify_salesforce_task(success, status, contact_id, invoicing_address, sp_id):
    tm = TaskManager()
    return tm.process_task(sp_id, 'NOTIFY SALESFORCE', success, lambda : update_contact(status, contact_id, invoicing_address))

@task(ignore_result=True)
def notify_tef_accounts_task(success, status, contact_id, sp_id):
    tm = TaskManager()
    return tm.process_task(sp_id, 'NOTIFY TEF ACCOUNT', success, lambda : (True, None))

@task(ignore_result=True)
def activate_contract_task(success, contract_id, sp_id):
    tm = TaskManager()
    return tm.process_task(sp_id, 'ACTIVATE CONTRACT', success, lambda : activate_contract(contract_id))

@task(ignore_result=True)
def generate_sdr_and_upload_task(success, tef_account, contract_id, sp_id):
    tm = TaskManager()
    return tm.process_task(sp_id, 'GENERATE SDR & UPLOAD', success, lambda : generate_and_upload_sdr(tef_account, contract_id))

@task(ignore_result=True)
def create_order_summary_task(success, sp_id):
    tm = TaskManager()
    
    invoice_json = tm.get_subprocess_data(sp_id)
    
    return tm.process_task(sp_id, 'CREATE ORDER SUMMARY', success, lambda : create_order_summary(invoice_json))
