from django.core.management.base import BaseCommand
from django.core.management.base import CommandParser
from django.utils import timezone

from typing import Dict, Optional, Any
from api.models import Listings

import csv
import datetime


class Command(BaseCommand):
    help: str = "Import Zillow listings data from specified CSV file into database"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("csv_file", type=str, help="CSV file path")

    def handle(self, *args: Any, **options: Dict[str, Any]) -> None:
        csv_file_path: str = options["csv_file"]
        self.stdout.write(self.style.SUCCESS(f"Starting import from {csv_file_path}"))

        num_success: int = 0
        num_error: int = 0
        try:
            with open(csv_file_path, "r", encoding="utf-8") as file:
                csv_reader: csv.DictReader = csv.DictReader(file)

                for row in csv_reader:
                    try:
                        updated_field: Dict[str, Any] = {}

                        listing: Listings = Listings(
                            bedrooms=self.process_int_field(row, "bedrooms"),
                            bathrooms=self.process_float_field(row, "bathrooms"),
                            home_size=self.process_int_field(row, "home_size"),
                            home_type=row["home_type"],
                            last_sold_date=self.process_date_field(
                                row, "last_sold_date"
                            ),
                            last_sold_price=self.process_int_field(
                                row, "last_sold_price"
                            ),
                            link=row["link"],
                            price=self.process_int_field(row, "price"),
                            property_size=self.process_int_field(row, "property_size"),
                            rent_price=self.process_int_field(row, "rent_price"),
                            rentzestimate_amount=self.process_int_field(
                                row, "rentzestimate_amount"
                            ),
                            rentzestimate_last_updated=self.process_date_field(
                                row, "rentzestimate_last_updated"
                            ),
                            tax_value=self.process_int_field(row, "tax_value"),
                            tax_year=self.process_int_field(row, "tax_year"),
                            year_built=self.process_int_field(row, "year_built"),
                            zestimate_amount=self.process_int_field(
                                row, "zestimate_amount"
                            ),
                            zestimate_last_updated=self.process_date_field(
                                row, "zestimate_last_updated"
                            ),
                            zillow_id=row["zillow_id"],
                            address=row["address"],
                            city=row["city"],
                            state=row["state"],
                            zipcode=row["zipcode"],
                        )
                        listing.save()
                        num_success += 1

                    except Exception as e:
                        num_error += 1
                        self.stdout.write(self.style.ERROR(f"Error importing row: {e}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error opening CSV file: {e}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"Command completed. successful imports: {num_success}, errors: {num_error}"
            )
        )

    def reverse_humanize_number(self, value: str) -> int:
        value = value.strip().replace("$", "").upper()

        if value.endswith("K"):
            return int(float(value[:-1]) * 1_000)
        elif value.endswith("M"):
            return int(float(value[:-1]) * 1_000_000)
        else:
            return int(float(value))

    def process_float_field(self, row: Dict[str, Any], float_field: str) -> float:
        try:
            if row[float_field] == "":
                return 0.0
            else:
                return float(row[float_field])
        except ValueError:
            self.stdout.write(
                self.style.WARNING(f"Invalid float: {float_field}: {row[float_field]}")
            )
            return 0

    def process_int_field(self, row: Dict[str, Any], int_field: str) -> int:
        try:
            value: str = row[int_field].lstrip("$")
            if value == "":
                return 0
            else:
                return self.reverse_humanize_number(value)
        except ValueError:
            self.stdout.write(
                self.style.WARNING(f"Invalid integer: {int_field}: {row[int_field]}")
            )
            return 0

    def process_date_field(
        self, row: Dict[str, Any], date_field: str
    ) -> Optional[datetime.datetime]:
        return self.convert_date_field(row, date_field)

    def convert_date_field(
        self, row: Dict[str, Any], field: str
    ) -> Optional[datetime.datetime]:
        new_date: Optional[datetime.datetime] = None
        if row[field] and row[field].strip():
            try:
                naive_datetime = datetime.datetime.strptime(
                    row[field].strip(), "%m/%d/%Y"
                )
                new_date = timezone.make_aware(naive_datetime)
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f"Date parsing error: {field}: {e}")
                )
        return new_date
