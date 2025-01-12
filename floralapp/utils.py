from django.db.models import TextField
from django.db.models.functions import Cast

from floralapp.models import Category, SubCategory, Product


def categories():
    return Category.objects.filter(active=True)


def subcategories(category_id):
    return SubCategory.objects.filter(fk_category_id=category_id, active=True)


def categories_list():
    categories_list = categories()
    data = {}
    for category in categories_list:
        subcategories_list = subcategories(category.id)
        temp = []
        if subcategories_list:
            for subcategory in subcategories_list:
                temp.append({
                    'name': subcategory.name,
                    'description': subcategory.description,
                    'id': subcategory.id,
                    'banner': subcategory.banner
                })
        if temp:
            data[category.name] = temp
    return data

def get_search_data(context: dict):
    try:
        subcategories = list(SubCategory.objects.annotate(str_id=Cast('id', output_field=TextField())).values('str_id', 'name'))
        products = list(Product.objects.annotate(str_id=Cast('id', output_field=TextField())).values('str_id', 'name'))
        context['subcategories'] = subcategories
        context['products'] = products
    except Exception:
        print("Error occur")
    return context

