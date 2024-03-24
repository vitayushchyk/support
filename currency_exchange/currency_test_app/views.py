# Create your views here.
import json

import requests
from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.views import View


class CurrencyMarket(View):
    def post(self, request):
        data = json.loads(request.body)
        from_currency, to_currency = data.get("from_currency"), data.get("to_currency")
        if not all([from_currency, to_currency]):
            raise ValueError("Missing from_currency or to_currency")
        cache_key = from_currency + to_currency
        if rate := cache.get(cache_key):
            print("fetched from cache")
            return JsonResponse({**data, "rate": rate})
        response_data = requests.get(
            f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}"
            f"&to_currency={to_currency}&apikey={settings.ALPHAVANTAGE_KEY}"
        )
        rate = float(
            response_data.json()["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
        )
        cache.set(cache_key, rate)

        return JsonResponse({**data, "rate": rate})
