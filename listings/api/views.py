from django.core import serializers
from django.http import JsonResponse
from api.models import Listings
import json

from .utils import convert_to_int


def query(request):
    try:
        field_names = [field.name for field in Listings._meta.fields]
        filter_kwargs = {}

        for param, value in request.GET.items():
            if param not in field_names:
                continue
            try:
                filter_obj = json.loads(value)
                if isinstance(filter_obj, dict):
                    for operator, filter_value in filter_obj.items():
                        if operator == "gt":
                            filter_kwargs[f"{param}__gt"] = filter_value
                        elif operator == "lt":
                            filter_kwargs[f"{param}__lt"] = filter_value
                        elif operator == "gte":
                            filter_kwargs[f"{param}__gte"] = filter_value
                        elif operator == "lte":
                            filter_kwargs[f"{param}__lte"] = filter_value
                        elif operator == "exact":
                            filter_kwargs[param] = filter_value
                else:
                    filter_kwargs[param] = value

            except json.JSONDecodeError:
                filter_kwargs[param] = value

        queryset = Listings.objects.filter(**filter_kwargs)
        data = serializers.serialize("json", queryset)
        return JsonResponse(json.loads(data), safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def get_listing_by_zillow_id(request, zillow_str):
    try:
        zillow_id = convert_to_int(zillow_str)
        if zillow_id == 0:
            return JsonResponse({"error": "invalid zillow_id"}, status=404)

        # Get the single listing
        listing = Listings.objects.get(zillow_id=zillow_id)
        data = serializers.serialize("json", [listing])
        return JsonResponse(json.loads(data), safe=False)
    except Listings.DoesNotExist:
        return JsonResponse({"error": "Listing not found"}, status=404)


def listings_query(request):
    data = {"message": "Hello, world!", "status": "success"}
    return JsonResponse(data)


def get_all_listings(request):
    listings = Listings.objects.all()
    data = serializers.serialize("json", listings)
    return JsonResponse(json.loads(data), safe=False)


def json_test(request):
    data = {"message": "test", "status": "success"}
    return JsonResponse(data)
