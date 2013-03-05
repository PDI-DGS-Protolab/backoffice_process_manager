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

from xhtml2pdf import pisa
from jinja2 import Template
from datetime import date

TEMPLATE_PATH = 'processes/pdf/template/invoice.html'
HEAD_PATH     = 'processes/pdf/template/head.jpg'

import codecs

from common.aws.s3 import upload_invoice_to_s3

def compute_invoice_details ():
    return {
            'number': "TF0000000088",
            'date':   unicode(date.today()),
            'head':   unicode(HEAD_PATH),
            'month':  unicode('January')
           }

def generate_pdf_and_upload(invoice_json):

    # Adding ".pdf" fo the name of the SDR file
    file_name = "{0}.pdf".format(invoice_json['sdr_file_name'])

    invoice_json['invoice'] = compute_invoice_details()

    pisa.showLogging()

    with codecs.open(TEMPLATE_PATH, 'r', 'utf-8') as f:
        template_content = f.read()

    template = Template(template_content)

    with open (file_name, "wb") as f:
        pdf = pisa.CreatePDF(template.render(invoice_json), f)

    if not pdf.err:
        upload_invoice_to_s3(file_name)

    invoice_json['pdf_file_name'] = file_name

    return (invoice_json, None)
