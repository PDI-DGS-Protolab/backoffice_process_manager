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
Created on 06/11/2012

@author: mac@tid.es
'''

from sforce.enterprise import SforceEnterpriseClient

from os import environ

SF_PRICELIST_ID = 'a13J0000000CtwvIAC'

def connect():
    c = SforceEnterpriseClient(environ.get('SF_WSDL_PATH'))
    c.login(environ.get('SF_LOGIN'), environ.get('SF_PWD'), environ.get('SF_TOKEN'))
    
    return c

def get_customers(account_id):
    
    c = connect()

    result = c.retrieve('Name, Email, MailingCountry, MailingPostalCode, MailingCity, MailingStreet, TefAccount__c',
                        'Contact', (account_id))

    return result

def get_catalogue():
    c = connect()
    
    soql = """SELECT Name, Price_per_Hour__c, Price_per_Month__c, Product_Code__c
              FROM Rate_Card_Item__c
              WHERE Rate_Card__c = '{0}'
            """.format(SF_PRICELIST_ID)

    results =  c.query(soql)
    
    catalogue = {}
    
    products = []
    
    for product in results.records:
        products.append({
                         'code'        : product.Product_Code__c, 
                         'description' : product.Name,
                         'price'       : product.Price_per_Hour__c
                         })
    
    catalogue['products'] = products
    
    return catalogue

def update_contact(status, contact_id):
    c = connect()

    print contact_id

    new_contact    = c.generateObject('Contact')
    new_contact.Id = contact_id

    new_contact.PaymentState__c = status

    c.update(new_contact)

    return (True, None)

def create_contract():
    c = connect()

    new_contract    = c.generateObject('Contract')
    
    new_contract.AccountId = "001d000000Wi4CBAAZ"
    new_contract.OwnerId   = "005d0000001LDCMAA4"
    new_contract.Status    = "Draft"
    
    new_contract.StartDate    = "2013-02-26"
    new_contract.ContractTerm = 12
    
    new_contract.CompanySignedId = "005d0000001LDCMAA4"
    new_contract.CustomerSignedId = "003d000000kC2JHAA0"
    
    result = c.create(new_contract)
    
    new_contract.Status = "Activated"
    new_contract.Id = result['id']
    
    print c.update(new_contract)

    return (True, None)
