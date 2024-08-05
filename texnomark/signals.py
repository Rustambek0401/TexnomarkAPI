import json
import os
# import json
# from aiogram.utils.json import json
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_delete
# from rest_framework.utils import json

from config.settings import BASE_DIR
from config.settings import DEFAULT_FROM_EMAIL
from texnomark.models import Product, Catalog, Category


def post_save_product(sender,instance,created,**kwargs):
    if created:
        print(f'Product {instance.product_name}  created ')
        subject = 'Product created'
        message = f'SIZNING BAZANGIZDA  => {instance.product_name} NOMLI Product YARATILDI '
        for_email = DEFAULT_FROM_EMAIL
        # to = 'nikola19testla98@gmail.com'
        to = 'jasurmavlonov24@gmail.com'

        send_mail(subject, message, for_email,[to,],fail_silently=False)
    else:
        print(f'Product {instance.product_name}  updated ')
post_save.connect(post_save_product,sender=Product)

def post_save_catalog(sender,instance,created,**kwargs):
    if created:
        print(f'Catalog {instance.catalog_name}  created ')
        subject = 'Catalog '
        message = f'SIZNING BAZANGIZDA  => {instance.catalog_name} NOMLI Catalog  YARATILDI '
        for_email = DEFAULT_FROM_EMAIL
        # to = 'nikola19testla98@gmail.com'
        to = 'jasurmavlonov24@gmail.com'

        send_mail(subject,message,for_email,[to,],fail_silently=False)
    else:
        print(f'Catalog {instance.catalog_name}  updated ')
post_save.connect(post_save_catalog, sender=Catalog)


# DELETE
def pre_delet_product(sender, instance, **kwargs):
    file_path = os.path.join(BASE_DIR, 'texnomark/delete/Product', f'Product{instance.product_name}.json')
    category_data = {
        'id': instance.id,
        'Name': instance.product_name,
        'Price':instance.price,
        'Description':instance.description,
        'Rating':instance.rating,
        'Discount':instance.discount,
        'Slug': instance.slug,
    }
    with open(file_path, 'w') as json_file:
        json.dump(category_data, json_file, indent=4)


    print(f'Product Ochirishdan oldin {instance.product_name}  json faylga saqlandi  ')
    subject = 'Product '
    message = f'SIZNING BAZANGIZDA  => {instance.product_name} NOMLI Product  O\'chirildi  VA texnomark/delete/Product papkaga malumotlar saqlandi'
    for_email = DEFAULT_FROM_EMAIL
    # to = 'nikola19testla98@gmail.com'
    to = 'jasurmavlonov24@gmail.com'

    send_mail(subject, message, for_email, [to, ], fail_silently=False)
pre_delete.connect(pre_delet_product, sender=Product)

def pre_delet_catalog(sender, instance, **kwargs):
    file_path = os.path.join(BASE_DIR, 'texnomark/delete/Catalog', f'Catalog{instance.id}.json')
    category_data = {
        'id': instance.id,
        'Name': instance.catalog_name,
        'Slug': instance.slug,
    }
    with open(file_path, 'w') as json_file:
        json.dump(category_data, json_file, indent=4)
    print(f'Catalog Ochirishdan oldin {instance.catalog_name}  json faylga saqlandi  ')

    subject = 'Catalog '
    message = f'SIZNING BAZANGIZDA  => {instance.catalog_name} NOMLI Catalog  O\'chirildi  VA texnomark/delete/Catalog papkaga malumotlar saqlandi '
    for_email = DEFAULT_FROM_EMAIL
    # to = 'nikola19testla98@gmail.com'
    to = 'jasurmavlonov24@gmail.com'
    send_mail(subject, message, for_email, [to, ], fail_silently=False)
pre_delete.connect(pre_delet_catalog, sender=Catalog)




def post_save_category(sender,instance,created,**kwargs):
    if created:
        print(f'Category {instance.category_name}  created ')
        subject = 'Category created'
        message = f'SIZNING BAZANGIZDA  => {instance.category_name} NOMLI Category YARATILDI '
        for_email = DEFAULT_FROM_EMAIL
        # to = 'nikola19testla98@gmail.com'
        to = 'jasurmavlonov24@gmail.com'

        send_mail(subject, message, for_email,[to,],fail_silently=False)
    else:
        print(f'Category {instance.category_name}  updated ')
post_save.connect(post_save_category,sender=Category)

def pre_delet_category(sender, instance, **kwargs):
    file_path = os.path.join(BASE_DIR, 'texnomark/delete/Category', f'category{instance.id}.json')
    category_data = {
        'id': instance.id,
        'Name': instance.category_name,
        'Slug': instance.slug,
    }
    with open(file_path, 'w') as json_file:
        json.dump(category_data, json_file, indent=4)
    print(f'Category Ochirishdan oldin {instance.category_name}  json faylga saqlandi  ')

    subject = 'Category '
    message = f'SIZNING BAZANGIZDA  => {instance.category_name} NOMLI Category  O\'chirildi  VA texnomark/delete/Category papkaga malumotlar saqlandi '
    for_email = DEFAULT_FROM_EMAIL
    # to = 'nikola19testla98@gmail.com'
    to = 'jasurmavlonov24@gmail.com'
    send_mail(subject, message, for_email, [to, ], fail_silently=False)
pre_delete.connect(pre_delet_category, sender=Category)

