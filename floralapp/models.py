import os
import uuid
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django_resized import ResizedImageField


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fk_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    banner = ResizedImageField(
        size=[1200, 400],
        quality=70,
        upload_to='banners/'
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fk_subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    discount_price = models.DecimalField(max_digits=15, decimal_places=2)
    view_count = models.PositiveIntegerField(default=0)
    product_image = ResizedImageField(
        size=[800, 800],
        quality=75,
        upload_to='products/',
        force_format='JPEG'
    )
    max_stock = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.product_image and not self.product_image.name.lower().endswith(".webp"):

            img_path = self.product_image.path
            img = Image.open(img_path)

            img = img.convert("RGB")
            img.thumbnail((800, 800))

            new_path = os.path.splitext(img_path)[0] + ".webp"

            img.save(new_path, "WEBP", quality=80)

            # delete old file
            os.remove(img_path)

            # update field path
            self.product_image.name = os.path.splitext(self.product_image.name)[0] + ".webp"

            super().save(update_fields=["product_image"])


class ProductImage(models.Model):
    fk_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = ResizedImageField(
        size=[800, 800],
        quality=75,
        upload_to='products/',
        force_format='JPEG'
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.fk_product.name}-{self.image.name}-{self.active}"

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        if self.image and not self.image.name.lower().endswith(".webp"):

            img_path = self.image.path
            img = Image.open(img_path)

            img = img.convert("RGB")
            img.thumbnail((800, 800))

            new_path = os.path.splitext(img_path)[0] + ".webp"

            img.save(new_path, "WEBP", quality=80)

            os.remove(img_path)

            self.image.name = os.path.splitext(self.image.name)[0] + ".webp"

            super().save(update_fields=["image"])
