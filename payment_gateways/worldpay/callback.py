from django.shortcuts import render
from django.db        import transaction

from payment_gateways.services import ServiceManager


class WorldpayCallbackController:

    serviceManager = ServiceManager()

    @classmethod
    def getCharger(cls):
        return cls.serviceManager.get_charger_by_name("ADYEN")

    @classmethod
    @transaction.commit_on_success
    def success(cls, request):
        return render(request, 'payment_gateways/success.html', {})

    @classmethod
    @transaction.commit_on_success
    def pending(cls, request):
        return render(request, 'payment_gateways/pending.html', {})

    @classmethod
    @transaction.commit_on_success
    def error(cls, request):
        return render(request, 'payment_gateways/error.html', {})
