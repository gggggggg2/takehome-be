from django.db import models


class Listings(models.Model):
    bathrooms = models.IntegerField()
    bedrooms = models.IntegerField()
    home_size = models.IntegerField()
    home_type = models.TextField()
    last_sold_date = models.DateTimeField(blank=True, null=True)
    last_sold_price = models.IntegerField()
    link = models.TextField()
    price = models.IntegerField()
    property_size = models.IntegerField()
    rent_price = models.IntegerField()
    rentzestimate_amount = models.IntegerField()
    rentzestimate_last_updated = models.DateTimeField(blank=True, null=True)
    tax_value = models.IntegerField()
    tax_year = models.IntegerField()
    year_built = models.IntegerField()
    zestimate_amount = models.IntegerField()
    zestimate_last_updated = models.DateTimeField(blank=True, null=True)
    zillow_id = models.TextField()
    address = models.TextField()
    city = models.TextField()
    state = models.TextField()
    zipcode = models.TextField()

    class Meta:
        managed = False
        db_table = "listings"
