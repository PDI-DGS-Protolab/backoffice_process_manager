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
from django.contrib import admin

from customers.models import Account
from datetime import datetime

from django.utils.timezone import utc

from django.core.files.base import ContentFile

STATUS = (
    ('OK',       'OK'),
    ('ERROR',    'ERROR'),
    ('CANCELED', 'CANCELED'),
    ('PENDING',  'PENDING'),
)

class BusinessProcess(models.Model):

    account = models.ForeignKey(Account)

    name = models.CharField(max_length = 100)

    start = models.DateTimeField(auto_now=True)
    end   = models.DateTimeField(blank=True, null=True)

    initial_data = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=10, choices=STATUS, default='PENDING')

    def __unicode__(self):
        return self.name

class SubProcess(models.Model):

    process = models.ForeignKey(BusinessProcess)

    name = models.CharField(max_length = 100)

    start = models.DateTimeField(auto_now=True)
    end   = models.DateTimeField(blank=True, null=True)

    status = models.CharField(max_length=10, choices=STATUS, default='PENDING')
    
    result = models.FileField(upload_to='processes', null=True)

    def __unicode__(self):
        return self.name

    def set_result(self, result):
        self.result.save('subprocess_{0}.json'.format(self.id), ContentFile(result))
        self.save()

class Task(models.Model):

    subprocess = models.ForeignKey(SubProcess)

    name = models.CharField(max_length = 100)

    start = models.DateTimeField(auto_now=True)
    end   = models.DateTimeField(blank=True, null=True)

    status = models.CharField(max_length=10, choices=STATUS, default='PENDING')

    remarkable_data = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def set_status(self, status):
        self.status = status
    
    def set_result(self, result):
        self.subprocess.set_result(result)

    def set_remarkable_data(self, remarkable_data):
        self.remarkable_data = remarkable_data

    def set_now_as_end(self):
        self.end = datetime.utcnow().replace(tzinfo=utc)

admin.site.register(BusinessProcess)
admin.site.register(SubProcess)
admin.site.register(Task)