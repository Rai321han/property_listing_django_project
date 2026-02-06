"""
Management command to import properties from CSV file
Usage: python manage.py import_properties <csv_file_path>
"""

import csv
from django.core.management.base import BaseCommand, CommandError
from property.models import Location


class Command(BaseCommand):
    help = "Import locations from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file", type=str, help="Path to the CSV file containing location data"
        )

    def handle(self, *args, **options):
        csv_file = options["csv_file"]

        try:
            with open(csv_file, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                # Validate required columns
                required_columns = ["name", "city", "state", "country"]

                if not all(col in reader.fieldnames for col in required_columns):
                    raise CommandError(
                        f'CSV must contain columns: {", ".join(required_columns)}'
                    )

                success_count = 0
                error_count = 0

                for row_num, row in enumerate(reader, start=2):
                    try:
                        # Create property
                        location_obj = Location.objects.create(
                            name=row["name"],
                            city=row["city"],
                            state=row["state"],
                            country=row["country"],
                        )

                        success_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Row {row_num}: Created property "{location_obj.name}"'
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
