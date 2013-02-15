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
Created on 16/10/2012

@author: mac@tid.es
'''


from common.aws.s3 import get_sdr_request_keys
from processes import start_order_to_cash_process, sync_order_to_cash, start_collections_process, models


def start_order_to_cash():
    keys = get_sdr_request_keys()

    for key in keys:
        start_order_to_cash_process(key)


def sync_first_order_to_cash():
    keys = get_sdr_request_keys()

    for key in keys:
        sync_order_to_cash(key)
        break


def start_collections(json):
    start_collections_process(json)


def get_processes_by_user(user_id):
    processes = models.BusinessProcess.objets.filter(tef_account=user_id)
    return processes


def get_subprocesses_by_process(process):
    subprocesses = process.SubProcess_set.all()
    return subprocesses


def get_tasks_by_subprocess(subprocess):
    tasks = subprocess.Task_set.all()
    return tasks
