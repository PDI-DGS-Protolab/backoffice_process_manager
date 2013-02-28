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
Created on 10/10/2012

@author: mac@tid.es
'''

from BeautifulSoup import BeautifulSoup

from common.aws.s3 import get_bucket_key_content

from catalogue import CATALOGUE, TAX

def round_price(price):
    return round(price*100)/100

def download_and_parse_sdr(bucket_key):
    xml = get_bucket_key_content(bucket_key)
    
    return parse_sdr(xml, bucket_key, CATALOGUE, TAX)

def parse_sdr(xml, file_name, catalogue, tax):
    doc = BeautifulSoup(xml)
    
    result = {}
    
    result['items']    = []
    result['subtotal'] = 0
        
    contracts  = doc.findAll('contrato')
    
    if (len(contracts) < 1):
        print "ERROR: NOT detected tos!!!"
        return
    
    first_contract = get_value(contracts[0])
    
    # Making sure all tos match!
    for contract in contracts:
        if (get_value(contract) != first_contract):
            print "ERROR: TOO MANY different tos!!!"
            return
    
    result['contract'] = str(first_contract)
    
    consumptions = doc.findAll('consumo_variable')
    
    for consumption in consumptions:
        concept = str(get_content(consumption, 'concepto_facturable'))
        amount = float(get_content(consumption, 'unidades'))
        
        price = float(get_price(catalogue, concept))
        description = get_description(catalogue, concept)
        
        invoice_entry = create_invoice_entry(concept, price, description, amount)
        
        result['items'].append(invoice_entry)
        
        result['subtotal'] += invoice_entry['total']
    
    # Computing subtotal
    result['total'] = round_price(tax * result['subtotal'])
    
    # Computing subtotal
    result['tax_rate'] = (tax - 1) * 100
    
    # Computing taxes
    result['taxes'] = round_price(result['total'] - result['subtotal'])
    
    # Adding file_name for naming PDF
    result['sdr_file_name'] = file_name
    
    return result

def create_invoice_entry(concept, price, description, amount):
    return {
            'concept': unicode(concept), 
            'price': price, 
            'description': unicode(description), 
            'amount': amount, 
            'total': round_price(price*amount)
            }

def get_value(element):
    return element.string

def get_price(catalogue, concept):
    if (catalogue.get(concept, -1) == -1):
        print("missing code: " + concept)
        return -1
        
    return catalogue[concept]['price']

def get_description(catalogue, concept):
    if (catalogue.get(concept, -1) == -1):
        print("missing code: " + concept)
        return ""
        
    return catalogue[concept]['description']


def get_content(consumption, fieldName):
    data = getattr(consumption, fieldName)
    
    if (not data):
        print("missing field: " + fieldName)
        return ""

    return data.string