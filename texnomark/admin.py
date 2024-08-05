from django.contrib import admin
from texnomark.models import (Category,
                          Catalog,
                          Product,
                          Image,
                          Comment,
                          Attribute,
                          AttributeValue,
                          PraductAttribute,
                        Address)
# Register your models here.
admin.site.register(Image)
# admin.site.register(Group)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(PraductAttribute)
admin.site.register(Address)
@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'slug']
    prepopulated_fields = {'slug': ('category_name',)}

@admin.register(Catalog)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['catalog_name', 'slug']
    prepopulated_fields = {'slug': ('catalog_name',)}

# @admin.register(Product)
# class CategoryModelAdmin(admin.ModelAdmin):
#     list_display = ['group_name', 'slug']
#     prepopulated_fields = {'slug': ('group_name',)}
