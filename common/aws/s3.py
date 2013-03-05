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



from boto.s3.connection import S3Connection
from boto.s3.key        import Key

from constants import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, SDR_REQUESTS_BUCKET, PDF_INVOICES_BUCKET

def connect():
    return S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

def get_sdr_request_keys():
    conn = connect()

    bucket = conn.get_bucket(SDR_REQUESTS_BUCKET)

    return bucket.list()

def get_bucket_key_content(key_name):

    conn = connect()

    bucket = conn.get_bucket(SDR_REQUESTS_BUCKET)

    key = bucket.lookup(key_name)

    return key.get_contents_as_string()

def upload_file_to_s3(file_name, bucket):
    conn = connect()

    bucket = conn.get_bucket(bucket)

    key = Key(bucket)

    key.key = file_name

    key.set_contents_from_filename(file_name)

def upload_invoice_to_s3(file_name):
    upload_file_to_s3(file_name, PDF_INVOICES_BUCKET)

def upload_sdr_to_s3(file_name):
    upload_file_to_s3(file_name, SDR_REQUESTS_BUCKET)
