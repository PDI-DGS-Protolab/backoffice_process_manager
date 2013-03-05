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
Created on 16/10/2012

@author: mac@tid.es
'''

from django.http        import HttpResponse
from django.shortcuts   import render
from django.http        import HttpResponseRedirect
from django.db          import transaction
from django.utils       import  simplejson

from services   import ServiceManager
from api_format import UserData

from django.views.decorators.csrf import csrf_exempt

class PaymentController:

    serviceManager = ServiceManager()

    @classmethod
    @transaction.commit_on_success
    @csrf_exempt
    def acquire_service(cls, request):

        if request.method == 'POST':

            body = request.body

            json = simplejson.loads(body)

            tef_account = json.get('tef_account', None)
            city        = json.get('city', None)
            address     = json.get('address', None)
            postal_code = json.get('postal_code', None)
            country     = json.get('country', None)
            phone       = json.get('phone', None)
            email       = json.get('email', None)
            gender      = json.get('gender', None)
            first_name  = json.get('first_name', None)
            last_name   = json.get('last_name', None)

            if (not tef_account or not city or not address or not postal_code or
                not country or not phone or not email or not gender or
                not first_name or not last_name):

                return HttpResponse('<h1>Insufficient parameters!</h1>', status=405)

            user_data = UserData(tef_account, city, address, postal_code, country, phone,
                                 email, gender, first_name, last_name)

            url = cls.serviceManager.generate_form_url(user_data)

            return HttpResponse(url, content_type='text/plain')
        else:
            return HttpResponse('<h1>Invalid Method</h1>', status=405)

    @classmethod
    def acquire_form(cls, request, token):

        if request.method == 'GET':

            user_data = cls.serviceManager.get_user_data_by_token(token)

            registered = cls.serviceManager.isPaymentDataRegistered(user_data)

            context = {
                        'code': token,
                        'email': user_data.email,
                        'address': user_data.address,
                        'postal_code': user_data.postal_code,
                        'country': user_data.country,
                        'city': user_data.city,
                        'last_name': user_data.last_name,
                        'first_name': user_data.first_name,
                        'gender': user_data.gender,
                        'registered': registered
                      }

            return render(request, 'payment_gateways/acquire_form.html', context)
        else:
            return HttpResponse('<h1>Invalid Method</h1>', status=405)

    @classmethod
    @transaction.commit_on_success
    def acquire_redirect(cls, request):

        if request.method == 'POST':

            params = request.POST.get

            token = params('token', None)

            # Storing user data in DB
            acquired_data  = cls.serviceManager.get_acquired_data_by_token(token)
            cls.serviceManager.update_acquired_data(params)

            # Checking if this user has already set up payment data
            registered = cls.serviceManager.isPaymentDataRegistered(acquired_data)

            # Creating inactive contract a
            contract_id = cls.serviceManager.createContract(acquired_data)

            if (not registered):
                # Start payment data acquisition flow
                url = cls.serviceManager.initial_payment_url(token, contract_id)
            else:
                # We already have payment data, so activating contract
                cls.serviceManager.data_acquisition_process.create_notify_acquired_data_process('Billable', acquired_data.tef_account,
                                                                                                contract_id, acquired_data)
                url = "/payment/gw/worldpay/success"

            return HttpResponseRedirect(url)
        else:
            return HttpResponse('<h1>Invalid Method</h1>', status=405)