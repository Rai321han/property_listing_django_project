"""
Management command to import properties from CSV file
Usage: python manage.py import_properties <csv_file_path>
"""

import csv
from django.core.management.base import BaseCommand, CommandError
from property.models import Property


class Command(BaseCommand):
    help = "Import properties from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file", type=str, help="Path to the CSV file containing property data"
        )

    def handle(self, *args, **options):
        csv_file = options["csv_file"]

        try:
            with open(csv_file, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                # Validate required columns
                required_columns = [
                    "title",
                    "description",
                    "property_type",
                    "status",
                    "price",
                    "bedrooms",
                    "bathrooms",
                ]

                if not all(col in reader.fieldnames for col in required_columns):
                    raise CommandError(
                        f'CSV must contain columns: {", ".join(required_columns)}'
                    )

                success_count = 0
                error_count = 0

                for row_num, row in enumerate(reader, start=2):
                    try:
                        # Get or create location
                        # location, created = Location.objects.get_or_create(
                        #     name=row["location_name"],
                        #     city=row["city"],
                        #     defaults={
                        #         "state": row.get("state", ""),
                        #         "country": row.get("country", "USA"),
                        #     },
                        # )

                        # Create property
                        property_obj = Property.objects.create(
                            title=row["title"],
                            description=row["description"],
                            # location=location,
                            property_type=row.get("property_type", "house"),
                            status=row.get("status", "available"),
                            price=float(row["price"]),
                            bedrooms=int(row["bedrooms"]),
                            bathrooms=float(row["bathrooms"]),
                        )

                        success_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Row {row_num}: Created property "{property_obj.title}"'
                            )
                        )

                    except Exception as e:
                        error_count += 1
                        self.stdout.write(
                            self.style.ERROR(f"Row {row_num}: Error - {str(e)}")
                        )

                # Summary
                self.stdout.write(
                    self.style.SUCCESS(
                        f"\nImport completed: {success_count} successful, {error_count} errors"
                    )
                )

        except FileNotFoundError:
            raise CommandError(f"CSV file not found: {csv_file}")
        except Exception as e:
            raise CommandError(f"Error reading CSV file: {str(e)}")
