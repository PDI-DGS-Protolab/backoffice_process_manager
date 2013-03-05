#!/usr/bin/python
#coding=utf-8

"""
Copyright 2012 Telefonica Investigacion y Desarrollo, S.A.U

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

"""
Created on 16/01/2013

@author: mac@tid.es
"""

import manage
import random
import unittest

# Loading environment variables prior to initialice django framework
manage.read_env('.env')
from django.test import TestCase

from customer.salesforce import get_customer_details_from_sf

from processes.notifications.sdr_gen import generate_and_upload_sdr
from common.salesforce.salesforce    import update_contact, create_contract, create_order_summary
from payment_gateways.api_format     import UserData

from os.path import exists

INVOICE = {
  "customer": {
    "city": "Madrid",
    "name": "Miguel Angel Ca\u00f1as Vaz",
    "tef_account": "003d000000wX82sAAC",
    "country": "BR",
    "postal_code": "28020",
    "address": "Lazaga n\u00ba13",
    "email": "mac@tid.es"
  },
  "tef_account": "003d000000wX82sAAC",
  "items": [
    {
      "total": 47.66,
      "amount": 259,
      "concept": "10052",
      "price": 0.184,
      "description": "Smart OS M 1vCPU - 4 GB"
    }
  ],
  "pdf_file_name": "003d000000wX82sAAC.xml.pdf",
  "contract": "800d00000001giTAAQ",
  "tax_rate": 20,
  "taxes": 9.53,
  "invoice": {
    "date": "2013-03-05",
    "head": "processes\/pdf\/template\/head.jpg",
    "number": "TF0000000088",
    "month": "January"
  },
  "total": 57.19,
  "subtotal": 47.66,
  "sdr_file_name": "003d000000wX82sAAC.xml"
}


class TestSalesforce(TestCase):

    @unittest.skip("Making tests faster")
    def test_salesforce_update_contact(self):

        result = update_contact('Billable', '003d000000lKGP2AAO')

        print result

    @unittest.skip("Making tests faster")
    def test_salesforce_get_gustomer(self):

        result = get_customer_details_from_sf('003d000000kC2JHAA0')

        print result

    @unittest.skip("Making tests faster")
    def test_salesforce_create_contract(self):

        user_data = UserData("003d000000wX82sAAC", "", "", "", "", "", "", "", "", "")

        result = create_contract(user_data, True)

        print result
    
    #@unittest.skip("Making tests faster")
    def test_salesforce_create_order_summary(self):
        
        result = create_order_summary(INVOICE)

        print result


class TestSDR(TestCase):

    #@unittest.skip("Making tests faster")
    def test_sdr(self):
        (result, file_name) = generate_and_upload_sdr("82822", "00010010101s")

        self.assertEqual(result, True, "Problem uploading SDR")

