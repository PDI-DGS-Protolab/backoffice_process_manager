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

from common.salesforce.salesforce import update_contact, activate_contract

from processes.task_manager import TaskManager

@task(ignore_result=True)
def notify_salesforce_task(success, status, contact_id, sp_id):
    tm = TaskManager()
    return tm.process_task(sp_id, 'NOTIFY SALESFORCE', success, lambda : update_contact(status, contact_id))

@task(ignore_result=True)
def notify_tef_accounts_task(success, status, contact_id, sp_id):
    tm = TaskManager()
    return tm.process_task(sp_id, 'NOTIFY TEF ACCOUNT', success, lambda : (True, None))

@task(ignore_result=True)
def activate_contract_task(success, status, contract_id, sp_id):
    tm = TaskManager()
    return tm.process_task(sp_id, 'ACTIVATE CONTRACT', success, lambda : activate_contract(None, contract_id))

