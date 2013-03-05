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

from models     import PaymentGateway, MasterInformation, Order, AcquiredData
from api_format import UserData

from processes.data_acquisition_process import DataAcquisitionProcess

from django.conf import settings

from common.salesforce.salesforce import create_contract

import importlib
import uuid


class ServiceManager:

    def __init__(self):
        self.data_acquisition_process = DataAcquisitionProcess()

    def isPaymentDataRegistered(self, user_data):
        tef_account = user_data.tef_account
        country     = user_data.country

        master_infos = MasterInformation.objects.filter(tef_account=tef_account, gateway__country=country, status = "VALIDATED")

        return len(master_infos) > 0

    def createContract(self, user_data):
        return create_contract(user_data)

    def initial_payment_url(self, token, contract_id):
        acquired_data = self.get_acquired_data_by_token(token)

        (charger, gw) = self.get_first_available_charger_by_country(acquired_data.country)
        if (charger == None):
            return "/error"

        url = charger.get_redirect_url(acquired_data)

        self.store_master_information(acquired_data, charger.get_order(), gw, contract_id)

        return url

    def get_charger_by_name(self, name):
        gw = self.get_gateway_by_name(name)

        if gw == None:
            return (None, None)

        return (self.dynamically_loading_charger(gw), gw)

    def get_first_available_charger_by_country(self, country):
        gw = self.get_gateway_by_country(country)

        if gw == None:
            return (None, None)

        return (self.dynamically_loading_charger(gw), gw)

    def get_charger_by_tef_account_and_country(self, tef_account, country):
        master_info = self.get_master_info_by_tef_account_and_country(tef_account, country)

        if master_info == None:
            return (None, None)

        gw = master_info.gateway

        return (self.dynamically_loading_charger(gw), master_info)

    def get_gateway_by_name(self, name):
        gws = PaymentGateway.objects.filter(name=name)

        if len(gws) == 0:
            return None

        return gws[0]

    def get_gateway_by_country(self, country):
        gws = PaymentGateway.objects.filter(country=country)

        if len(gws) == 0:
            return None

        # If several, getting the first one
        return gws[0]

    def get_master_info_by_tef_account_and_country(self, tef_account, country):
        master_infos = MasterInformation.objects.filter(tef_account=tef_account, gateway__country=country)

        if len(master_infos) == 0:
            return None

        # If several, getting the first one
        return master_infos[0]

    def get_charger_by_master_information(self, country):
        gw = self.get_gateway_by_country(country)

        if gw == None:
            return None

        return self.dynamically_loading_charger(gw)

    def process_recurrent_payment(self, order_data):

        self.store_order(order_data)

        tef_account = order_data.tef_account
        country     = order_data.country

        (charger, master_info) = self.get_charger_by_tef_account_and_country(tef_account, country)
        if charger == None:
            return False

        charger.recurrent_payment(order_data, master_info)

        return True


    def store_master_information(self, acquired_data, recurrent_order_code, gateway, contract_id):
        # Creating subprocese
        subprocess = self.data_acquisition_process.create_acquire_data_subprocess(acquired_data.tef_account)

        # Linking master info and subprocess
        master_info = MasterInformation( tef_account=acquired_data.tef_account, recurrent_order_code=recurrent_order_code,
                                         gateway=gateway, email=acquired_data.email, subprocess=subprocess, contract=contract_id,
                                         acquired_data=acquired_data)
        master_info.save()

    def store_order(self, order_data):
        order = Order(total=order_data.total, currency=order_data.currency, country=order_data.country,
                      tef_account=order_data.tef_account, statement=order_data.statement,
                      order_code=order_data.order_code)

        order.save()


    def dynamically_loading_charger(self, gw):
        charger_module = importlib.import_module(gw.module_name)
        charger = getattr(charger_module, gw.class_name)(gw)

        return charger

    def generate_form_url(self, user_data):
        token = self.compute_unique_id()

        acquired_data = AcquiredData(tef_account=user_data.tef_account, email=user_data.email,
                                     city=user_data.city, address=user_data.address,
                                     postal_code=user_data.postal_code, country=user_data.country,
                                     token=token, gender=user_data.gender, first_name=user_data.first_name,
                                     last_name=user_data.last_name)

        acquired_data.save()

        url = settings.DEPLOY_URL + "/payment/acquire/form/" + token

        return url

    def get_user_data_by_token(self, token):
        acquired_data = AcquiredData.objects.get(token=token)

        user_data = UserData(acquired_data.tef_account, acquired_data.city, acquired_data.address,
                             acquired_data.postal_code, acquired_data.country, acquired_data.phone, acquired_data.email,
                             acquired_data.gender, acquired_data.first_name, acquired_data.last_name)

        return user_data

    def get_acquired_data_by_token(self, token):
        acquired_data = AcquiredData.objects.get(token=token)

        return acquired_data

    def update_acquired_data(self, params):
        token = params('token', None)

        acquired_data = AcquiredData.objects.get(token=token)

        acquired_data.address     = params('address', None)
        acquired_data.city        = params('city', None)
        acquired_data.postal_code = params('postal_code', 454)

        acquired_data.save()

    def compute_unique_id(self):
        uid = uuid.uuid4()
        return uid.hex[:10]

