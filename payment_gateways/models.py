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
Created on 16/10/2012

@author: mac@tid.es
'''

from django.db import models

from processes.models import SubProcess

STATUS = (
    ('PENDING',   'PENDING'),
    ('VALIDATED', 'VALIDATED'),
    ('ERROR',     'ERROR'),
    ('CANCELED',  'CANCELED'),
)

class PaymentGateway(models.Model):

    name = models.CharField(max_length = 100)

    endpoint = models.CharField(max_length = 200)

    success_callback = models.CharField(max_length = 200)
    error_callback   = models.CharField(max_length = 200)
    pending_callback = models.CharField(max_length = 200)

    merchant = models.CharField(max_length = 20)
    password = models.CharField(max_length = 20)

    module_name = models.CharField(max_length = 200)
    class_name  = models.CharField(max_length = 50)
    
    country    = models.CharField(max_length = 3)

class MasterInformation(models.Model):

    gateway     = models.ForeignKey(PaymentGateway)
    
    tef_account = models.CharField(max_length = 20)
    email       = models.EmailField(blank=True)
    
    recurrent_order_code = models.CharField(max_length=10)
    
    status = models.CharField(max_length=10, choices=STATUS, default='PENDING')
    
    subprocess = models.ForeignKey(SubProcess, null=True)
    contract = models.CharField(max_length = 20)

class Order(models.Model):

    total    = models.IntegerField()
    currency = models.CharField(max_length = 3)
    country  = models.CharField(max_length = 3)
    
    order_code  = models.CharField(max_length=10)
    tef_account = models.CharField(max_length = 20)

    statement = models.CharField(max_length = 200)

    status = models.CharField(max_length=10, choices=STATUS, default='PENDING')
    result = models.TextField()

class AcquiredData(models.Model):

    tef_account = models.CharField(max_length = 20)
    email       = models.EmailField(blank=True)

    gender      = models.CharField(max_length = 100)

    first_name  = models.CharField(max_length = 100)
    last_name   = models.CharField(max_length = 100)

    city        = models.CharField(max_length = 100)
    address     = models.CharField(max_length = 200)
    postal_code = models.CharField(max_length = 10)
    country     = models.CharField(max_length = 3)
    phone       = models.CharField(max_length = 10)

    token = models.CharField(unique=True, max_length=10)