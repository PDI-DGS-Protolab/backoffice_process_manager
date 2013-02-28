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

from notifications.tasks  import notify_salesforce_task, notify_tef_accounts_task, activate_contract_task

class DataAcquisitionProcess:

    def __init__(self):
        pass

    def create_acquire_data_subprocess(self, tef_account):
        return self._generate_acquire_data_subprocess(tef_account)

    def start_notify_acquired_data(self, status, master_info):
        contact_id  = master_info.tef_account
        subprocess  = master_info.subprocess
        contract_id = master_info.contract

        sp_id = subprocess.id

        chain = activate_contract_task.s(True, contract_id, sp_id) | notify_salesforce_task.s(status, contact_id, sp_id) | notify_tef_accounts_task.s(status, contact_id, sp_id)

        chain()

    def sync_notify_acquired_data(self, status, master_info):
        contact_id = master_info.tef_account

        subprocess = master_info.subprocess

        sucess = notify_salesforce_task(True, status, contact_id, subprocess.id)
        sucess = notify_tef_accounts_task(sucess, status, contact_id, subprocess.id)

        return sucess

    def _generate_notify_acquired_data_subprocess(previous_subprocess):
        process = BusinessProcess.objects.get(id=previous_subprocess)

        sub_process = SubProcess(process=process, name='NOTIFY ACQUIRED DATA')
        sub_process.save()

        return sub_process

    def _generate_acquire_data_subprocess(self, tef_account):
        process = BusinessProcess(tef_account=tef_account, name='ACQUIRE PAYMENT DATA')
        process.save()

        sub_process = SubProcess(process=process, name='ACQUIRE DATA')
        sub_process.save()

        return sub_process