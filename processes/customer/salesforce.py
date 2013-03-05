#!/usr/bin/python
#coding=utf-8 

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
Created on 31/10/2012

@author: mac@tid.es
'''

from common.salesforce.salesforce import get_customers

def get_customer_details_from_sf(account_id):
    
    contact = get_customers(account_id)
    
    if not contact:
        return {}

    return {
            'name'       : unicode(contact.Name[0]),
            'address'    : unicode(contact.MailingStreet[0]),
            'city'       : unicode(contact.MailingCity[0]),
            'postal_code': unicode(contact.MailingPostalCode[0]),
            'email'      : unicode(contact.Email[0]),
            'country'    : unicode(contact.MailingCountry[0]),
            'tef_account': unicode(contact.TefAccount__c[0])
    }

def customer_details_from_sf(invoice_json):
    account_id = invoice_json['tef_account']
    
    # Adding customer details
    invoice_json['customer'] = get_customer_details_from_sf(account_id)
    
    return (invoice_json, None)