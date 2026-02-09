import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File

from property.models import Property, Image


class Command(BaseCommand):
    help = "Assign property images to properties (2 per property, rest to last)"

    def handle(self, *args, **kwargs):
        image_dir = os.path.join(settings.MEDIA_ROOT, "property_images")

        if not os.path.exists(image_dir):
            self.stderr.write("❌ property_images folder not found")
            return

        image_files = sorted(
            [
                f
                for f in os.listdir(image_dir)
                if f.lower().endswith((".jpg", ".jpeg", ".png"))
            ]
        )

        properties = list(Property.objects.all().order_by("id"))

        if not properties:
            self.stderr.write("❌ No properties found")
            return

        if not image_files:
            self.stderr.write("❌ No images found")
            return

        img_index = 0
        total_images = len(image_files)

        for i, prop in enumerate(properties):
            images_for_this_property = 2

            # If this is the last property, give it all remaining images
            if i == len(properties) - 1:
                images_for_this_property = total_images - img_index

            for _ in range(images_for_this_property):
                if img_index >= total_images:
                    break

                image_name = image_files[img_index]
                image_path = os.path.join(image_dir, image_name)

                with open(image_path, "rb") as f:
                    django_file = File(f, name=image_name)
                    Image.objects.create(
                        property=prop,
                        image=django_file,
                        is_primary=(prop.images.count() == 0),
                        order=prop.images.count(),
                    )

                img_index += 1

            self.stdout.write(f"✅ Assigned images to {prop.title}")

        self.stdout.write(self.style.SUCCESS("🎉 Image seeding completed"))
