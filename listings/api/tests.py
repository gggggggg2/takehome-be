from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

import json
from datetime import datetime
from .models import Listings


class ListingsTestCase(TestCase):

    def setUp(self):
        Listings.objects.create(
            bathrooms=2.5,
            bedrooms=3,
            home_size=2000,
            home_type="Single Family",
            last_sold_date=timezone.make_aware(datetime(2020, 1, 15)),
            last_sold_price=500000,
            link="https://example.com/home1",
            price=550000,
            property_size=5000,
            rent_price=3000,
            rentzestimate_amount=2800,
            rentzestimate_last_updated=timezone.make_aware(datetime(2023, 6, 1)),
            tax_value=480000,
            tax_year=2022,
            year_built=1995,
            zestimate_amount=540000,
            zestimate_last_updated=timezone.make_aware(datetime(2023, 6, 1)),
            zillow_id="123456",
            address="123 Somewhere St",
            city="Newark",
            state="CA",
            zipcode="94536",
        )

        Listings.objects.create(
            bathrooms=1.5,
            bedrooms=2,
            home_size=1200,
            home_type="Condo",
            last_sold_date=timezone.make_aware(datetime(2021, 3, 20)),
            last_sold_price=300000,
            link="https://example.com/home2",
            price=325000,
            property_size=1500,
            rent_price=1800,
            rentzestimate_amount=1750,
            rentzestimate_last_updated=timezone.make_aware(datetime(2023, 6, 2)),
            tax_value=290000,
            tax_year=2022,
            year_built=2005,
            zestimate_amount=320000,
            zestimate_last_updated=timezone.make_aware(datetime(2023, 6, 2)),
            zillow_id="654321",
            address="456 Oak Ave",
            city="Fremont",
            state="CA",
            zipcode="94539",
        )

        self.client = Client()

    def test_get_all_listings(self):
        response = self.client.get(reverse("get_all_listings"))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)

    def test_get_listing_by_zillow_id(self):
        response = self.client.get(reverse("get_listing_by_zillow_id", args=["123456"]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["fields"]["address"], "123 Main St")

    def test_get_listing_by_invalid_zillow_id(self):
        response = self.client.get(
            reverse("get_listing_by_zillow_id", args=["invalid"])
        )
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertEqual(data["error"], "invalid zillow_id")

    def test_get_listing_by_nonexistent_zillow_id(self):
        response = self.client.get(reverse("get_listing_by_zillow_id", args=["999999"]))
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertEqual(data["error"], "Listing not found")

    def test_query_exact_match(self):
        response = self.client.get("/api/query/?bedrooms=2")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["fields"]["address"], "456 Oak Ave")

    def test_query_range_filters(self):
        query_params = {
            "bedrooms": json.dumps({"gt": 1, "lt": 4}),
            "rentzestimate_amount": json.dumps({"gt": 1000, "lt": 2000}),
        }
        response = self.client.get("/api/query/", query_params)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["fields"]["address"], "456 Oak Ave")

    def test_query_multiple_conditions(self):
        query_params = {
            "bathrooms": json.dumps({"gte": 2}),
            "year_built": json.dumps({"lt": 2000}),
        }
        response = self.client.get("/api/query/", query_params)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["fields"]["address"], "123 Main St")

    def test_query_no_results(self):
        query_params = {"bedrooms": json.dumps({"gt": 5})}
        response = self.client.get("/api/query/", query_params)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 0)

    def test_query_invalid_json(self):
        response = self.client.get("/api/query/?bedrooms={invalid_json}")
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn("error", data)

    def test_query_invalid_field(self):
        response = self.client.get('/api/query/?invalid_field={"gt": 1}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(
            len(data), 2
        )  # Should return all listings, ignoring an invalid field

    def test_json_test_view(self):
        response = self.client.get(reverse("json_test"))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["message"], "test")
        self.assertEqual(data["status"], "success")


class UtilsTestCase(TestCase):
    def test_convert_to_int_with_valid_string(self):
        from .utils import convert_to_int

        result = convert_to_int("123")
        self.assertEqual(result, 123)

    def test_convert_to_int_with_invalid_string(self):
        from .utils import convert_to_int

        result = convert_to_int("abc")
        self.assertEqual(result, 0)

    def test_convert_to_int_with_none(self):
        from .utils import convert_to_int

        result = convert_to_int(None)
        self.assertEqual(result, 0)
