from floralapp.models import Category, SubCategory


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
                })
        if temp:
            data[category.name] = temp
    return data
