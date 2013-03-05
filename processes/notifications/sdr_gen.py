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

@author: ablazquez@conwet.com
@author: sperez@conwet.com
'''

import datetime
import random

from common.aws.s3 import upload_sdr_to_s3

import os

def gen_sdr(tef_account, contract_id):
    now = str(datetime.datetime.now())
    consumption = random.randint(1, 300)

    print tef_account
    print contract_id

    xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                <fichero_consumos_variables>
                <fecha_envio>{0}</fecha_envio>
                <consumos_variables total_registros="4">
                    <consumo_variable>
                        <id>{1}</id>
                        <contrato>{2}</contrato>
                        <servicio_comercial>0</servicio_comercial>
                        <concepto_facturable>10052</concepto_facturable>
                        <fecha_consumo>2012-07Z</fecha_consumo>
                        <unidades>{3}</unidades>
                        <posicion>1</posicion>
                        <total_posiciones>1</total_posiciones>
                    </consumo_variable>
                </consumos_variables>
                </fichero_consumos_variables>
          """.format(now, tef_account, contract_id, consumption)

    file_name = tef_account + ".xml"

    with open(file_name, 'w') as f:
        f.write(xml)

    return file_name

def generate_and_upload_sdr(tef_account, contract_id):
    file_name = gen_sdr(tef_account, contract_id)

    upload_sdr_to_s3(file_name)

    return (True, file_name)


