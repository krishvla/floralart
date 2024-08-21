import random
import time

from django.core.management.base import BaseCommand, CommandError
from floralapp.models import *
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile


class Command(BaseCommand):
    help = "Generates the Dummy Initial Data"

    def save_banner_image_from_url(self, url, instance):
        # Download the image
        img_temp = NamedTemporaryFile(delete=True)
        response = requests.get(url)
        img_temp.write(response.content)
        img_temp.flush()

        # Save it to the model
        instance.banner.save(f"image_{instance.pk}.jpg", File(img_temp))
        instance.save()

    def save_product_image_from_url(self, url, instance):
        # Download the image
        img_temp = NamedTemporaryFile(delete=True)
        response = requests.get(url)
        img_temp.write(response.content)
        img_temp.flush()

        # Save it to the model
        instance.product_image.save(f"image_{instance.pk}.jpg", File(img_temp))
        instance.save()

    def save_image_from_url(self, url, instance):
        # Download the image
        img_temp = NamedTemporaryFile(delete=True)
        response = requests.get(url)
        img_temp.write(response.content)
        img_temp.flush()

        # Save it to the model
        instance.image.save(f"image_{instance.pk}.jpg", File(img_temp))
        instance.save()

    def handle(self, *args, **options):
        images_urls_list = [
            "https://img.freepik.com/premium-vector/seamless-pattern-tropical-nature-background-with-hand-draw-floral-leaves_42350-656.jpg",
            "https://img.freepik.com/premium-vector/seamless-floral-pattern_42350-292.jpg",
            "https://img.freepik.com/premium-photo/wallpaper-tropical-flowers-pineapple-graphics-painting_53876-253706.jpg"
            "https://img.freepik.com/free-vector/2d-tropical-flowers-background_52683-8345.jpg",
            "https://img.freepik.com/free-vector/tropical-flowers-leaves-background-zoom_52683-40396.jpg",
            "https://img.freepik.com/free-photo/flat-lay-tulips-colored-background_169016-20268.jpg",
            "https://img.freepik.com/free-photo/blank-paper-envelope-wooden-background-with-eucalyptus-twigs-flat-lay_169016-27412.jpg",
            "https://img.freepik.com/free-photo/flower-wallpaper-that-says-flower-it_1340-37282.jpg"
        ]
        categiries_data = [
            {
                "name": "Pooja Items",
                "description": "Pooja Items",
                "sub_categoriess": [
                    {
                        "name": "Varamahalalkshmi Pooja Items",
                        "description": """Varamahalalkshmi Pooja Items. \n dummy description""",
                        "banner": "https://img.freepik.com/free-photo/closeup-textural-bright-exotic-flowers-generative-al_169016-28576.jpg"
                    },
                    {
                        "name": "German Silver Pooja Items",
                        "description": """German Silver Pooja Items. \n dummy description""",
                        "banner": "https://img.freepik.com/premium-vector/hand-drawn-vintage-floral-background_42350-382.jpg"
                    }
                ]
            },
            {
                "name": "BackDrop Collection",
                "description": "BackDrop Collection",
                "sub_categoriess": [
                    {
                        "name": "Back Drop Props",
                        "description": """Back Drop Props Items. \n dummy description""",
                        "banner": "https://img.freepik.com/free-photo/stage-with-white-curtain-that-says-pink-white-it_1340-24739.jpg"
                    },
                    {
                        "name": "Backdrop Decoration Sets",
                        "description": """Backdrop Decoration Sets Items. \n dummy description""",
                        "banner": "https://m.media-amazon.com/images/I/81YkgPDYu-L.jpg"
                    },
                    {
                        "name": "Foam Boards Sets",
                        "description": """Foam Boards Sets Items. \n dummy description""",
                        "banner": "https://5.imimg.com/data5/SELLER/Default/2023/3/296707769/BN/VE/ET/533004/pvc-foam-board-sheet-500x500.jpg"
                    }
                ]
            },
            {
                "name": "Decoration Collection",
                "description": "BackDrop Collection",
                "sub_categoriess": [
                    {
                        "name": "Lilly Strings",
                        "description": """Lilly Strings Items. \n dummy description""",
                        "banner": "https://img.freepik.com/free-photo/stage-with-white-curtain-that-says-pink-white-it_1340-24739.jpg"
                    },
                    {
                        "name": "Fabric Garlands Sets",
                        "description": """Fabric Garlands Sets Items. \n dummy description""",
                        "banner": "https://m.media-amazon.com/images/I/81YkgPDYu-L.jpg"
                    },
                    {
                        "name": "Palm Leaf Sets",
                        "description": """Palm Leaf Sets Items. \n dummy description""",
                        "banner": "https://5.imimg.com/data5/SELLER/Default/2023/3/296707769/BN/VE/ET/533004/pvc-foam-board-sheet-500x500.jpg"
                    }
                ]
            },
            {
                "name": "Home Decor",
                "description": "BackDrop Collection",
                "sub_categoriess": [
                    {
                        "name": "Rangoli Mats",
                        "description": """Rangoli Mats Items. \n dummy description""",
                        "banner": "https://img.freepik.com/free-photo/stage-with-white-curtain-that-says-pink-white-it_1340-24739.jpg"
                    },
                    {
                        "name": "Bananna Tree Stands Sets",
                        "description": """Fabric Garlands Sets Items. \n dummy description""",
                        "banner": "https://m.media-amazon.com/images/I/81YkgPDYu-L.jpg"
                    }
                ]
            }
        ]

        for category in categiries_data:
            print("Saving Category '{}'".format(category['name']))
            category_obj, _ = Category.objects.get_or_create(name=category["name"], description=category["description"])
            for sub_category in category["sub_categoriess"]:
                print("Saving Sub-Category '{}'".format(sub_category['name']))
                sub_category_obj, _ = SubCategory.objects.get_or_create(
                    fk_category=category_obj, name=sub_category["name"],
                    defaults={
                        "description": sub_category["description"]
                    }
                )
                self.save_banner_image_from_url(sub_category["banner"], sub_category_obj)

                #creatiing products
                print("Creating Products")
                for i in range(3):
                    product_obj = Product.objects.create(
                        fk_subcategory=sub_category_obj,
                        sku=f"SKU-{time.time()}-{sub_category_obj.name}-000{i}",
                        name=f"{sub_category['name']}-Item-{i}",
                        description="Dummy Description\nDummy Description",
                        price=100*i,
                        discount_price=100*i - (100*i/10),
                        max_stock=10*i,
                    )
                    print("Saving product Image")
                    self.save_product_image_from_url( random.choice(images_urls_list), product_obj)

                    for j in range(3):
                        print("Saving products all images")
                        product_img_obj = ProductImage.objects.create(fk_product=product_obj)
                        self.save_image_from_url(random.choice(images_urls_list), product_img_obj)


