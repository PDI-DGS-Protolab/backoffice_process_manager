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

from services   import initial_payment_url, generate_form_url, get_user_data_by_token
from api_format import UserData

from django.views.decorators.csrf import csrf_exempt

@transaction.commit_on_success
@csrf_exempt
def acquire_service(request):

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

        url = generate_form_url(user_data)

        return HttpResponse(url, content_type='text/plain')
    else:
        return HttpResponse('<h1>Invalid Method</h1>', status=405)


def acquire_form(request, token):

    if request.method == 'GET':

        user_data = get_user_data_by_token(token)

        context = {
                    'code': token,
                    'email': user_data.email,
                    'address': user_data.address,
                    'postal_code': user_data.postal_code,
                    'country': user_data.country,
                    'city': user_data.city,
                    'last_name': user_data.last_name,
                    'first_name': user_data.first_name,
                    'gender': user_data.gender
                  }

        return render(request, 'payment_gateways/acquire_form.html', context)
    else:
        return HttpResponse('<h1>Invalid Method</h1>', status=405)

@transaction.commit_on_success
def acquire_redirect(request):

    if request.method == 'POST':

        params = request.POST.get

        token = params('token', None)
        
        url = initial_payment_url(token)
    
        return HttpResponseRedirect(url)
    else:
        return HttpResponse('<h1>Invalid Method</h1>', status=405)