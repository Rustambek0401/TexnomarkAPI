from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    category_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)

        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name

class Product(BaseModel):
    class RatingChoices(models.IntegerChoices):
        nol = 0
        bir = 1
        ikki = 2
        uch = 3
        tort = 4
        besh = 5

    product_name = models.CharField(max_length=299, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(choices=RatingChoices.choices, default=RatingChoices.besh.value, null=True, blank=True)
    discount = models.IntegerField(default=0)
    slug = models.SlugField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product',null=True,blank=True)
    users_like = models.ManyToManyField(User, related_name='users_like',blank=True,db_table='User_Like')

    @property
    def discounted_price(self):
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)

        return self.price

    @property
    def pay_monthly_6(self):
        return self.price / 6

    @property
    def pay_monthly_12(self):
        return self.price / 12

    @property
    def pay_monthly_24(self):
        return self.price / 24

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name



class Catalog(BaseModel):
    catalog_name = models.CharField(max_length=199, unique=True)
    slug = models.SlugField(null=True, blank=True)
    product = models.ManyToManyField(Product,related_name='product')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.catalog_name)

        super(Catalog, self).save(*args, **kwargs)

    def __str__(self):
        return self.catalog_name



class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_images', null=True, blank=True)

    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = 'Image'

class Comment(BaseModel):
    class Reting(models.IntegerChoices):
        bir = 1
        ikki = 2
        uch = 3
        tort = 4
        besh = 5
    reting = models.IntegerField(choices=Reting.choices, default=Reting.besh.value, null=True, blank=True)
    advantages = models.TextField(null=True,blank=True)
    disadvantages = models.TextField(null=True,blank=True)
    your_comment = models.TextField(null=True,blank=True)
    file = models.FileField(upload_to='communts/',null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Attribute(models.Model):
    attribute_name = models.CharField(max_length=200)
    def __str__(self):
        return self.attribute_name
class AttributeValue(models.Model):
    attribute_value = models.CharField(max_length=200)
    def __str__(self):
        return self.attribute_value

class PraductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='atribut')
    key = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='key')
    value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE, related_name='value')


class Address(BaseModel):
    address = models.CharField(max_length=599)
    work_order = models.CharField(max_length=399)
    phone = models.CharField(max_length=39)
