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
Created on 30/10/2012

@author: mac@tid.es
'''

from django.shortcuts import render
from django.db        import transaction


from services import ProcessManager

class ProcessesController:

    processManager = ProcessManager()

    @classmethod
    @transaction.commit_on_success
    def launch_invoicing(cls, request):
        cls.processManager.start_order_to_cash()

        return render(request, 'processes/invoicing.html', {})

    @classmethod
    @transaction.commit_on_success
    def launch_sync_invoice(cls, request):
        cls.processManager.sync_first_order_to_cash()

        return render(request, 'processes/invoicing.html', {})

    @classmethod
    @transaction.commit_on_success
    def launch_provision(cls, request):
        cls.processManager.start_provision('tef_account_127', {})

        return render(request, 'processes/running.html', {})

    @classmethod
    @transaction.commit_on_success
    def get_processes(cls, request, user_id):

        processes = cls.processManager.get_processes_by_user(user_id)

        subprocesses = {}
        tasks = {}

        for process in processes:
            subprocess = cls.processManager.get_subprocesses_by_process(process)
            subprocesses[process] = subprocess

            for sub in subprocess:
                tasks[sub] = cls.processManager.get_tasks_by_subprocess(sub)

        args = {
            "processes"   : processes,
            "subprocesses": subprocesses,
            "tasks"       : tasks
            }
        return render(request, 'processes/processes.html', args)
