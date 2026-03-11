import os
from PIL import Image
from django.core.management.base import BaseCommand
from floralapp.models import Product, ProductImage


class Command(BaseCommand):
    help = "Convert existing images to WebP and resize to 800x800"

    def convert_image(self, image_field):

        if not image_field:
            return None

        if image_field.name.lower().endswith(".webp"):
            return None

        old_path = image_field.path

        img = Image.open(old_path)
        img = img.convert("RGB")
        img.thumbnail((800, 800))

        new_path = os.path.splitext(old_path)[0] + ".webp"

        img.save(new_path, "WEBP", quality=80)

        os.remove(old_path)

        return os.path.splitext(image_field.name)[0] + ".webp"

    def handle(self, *args, **kwargs):

        for product in Product.objects.all():

            new_name = self.convert_image(product.product_image)

            if new_name:
                product.product_image.name = new_name
                product.save(update_fields=["product_image"])

                self.stdout.write(f"Converted product {product.id}")

        for img in ProductImage.objects.all():

            new_name = self.convert_image(img.image)

            if new_name:
                img.image.name = new_name
                img.save(update_fields=["image"])

                self.stdout.write(f"Converted product image {img.id}")

        self.stdout.write(self.style.SUCCESS("Image optimization completed"))