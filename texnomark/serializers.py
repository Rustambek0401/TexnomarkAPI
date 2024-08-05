from django.contrib.auth.models import User
from django.db.models import Avg
from django.db.models import Avg
from django.db.models.functions import Round
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

from texnomark.models import (Image,
                              Category,
                              Catalog,
                              Product,
                              Comment,
                              PraductAttribute,
                              Attribute,
                              AttributeValue, Address, )


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class AtributSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'

class AtributValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = '__all__'



class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['id','image','is_primary','category','group','product']
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ()

class ProductSerialize(serializers.ModelSerializer):
    all_image = serializers.SerializerMethodField()
    # catalog = serializers.CharField(source='catalog.catalog_name', read_only=True)
    category = serializers.CharField(source='category.category_name', read_only=True)
    product_images = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    # atribut = ProductAtriburSerializer(many=True,read_only=True)
    atributs = serializers.SerializerMethodField()
    # comment = CommentSerializer(many=True, read_only=True)

    def get_atributs(self,instance):
       # atribut = PraductAttribute.objects.filter(product = instance).values_list('key','key__attribute_name','value_id','value__attribute_value')
        atribut = instance.atribut.values_list('key','key__attribute_name','value_id','value__attribute_value')
        characters = [
            {
                'atribut_id':key_id,
                'atribut_name':key_name,
                'atribut_value_id':value_id,
                'atribut_value_name':value_name
            }
            for key_id, key_name, value_id, value_name in atribut
        ]
        return characters
    #

    def get_avg_rating(self,obj):
        # avg_rating = Comment.objects.filter(product=obj).aggregate(avg_rating=Round(Avg('reting')))
        avg_rating = obj.comments.aggregate(avg_rating=Round(Avg('reting')))
        if avg_rating.get('avg_rating'):
            return avg_rating.get('avg_rating')
        else:
            return 0

    def get_comments_count(self,instance):
        # count = Comment.objects.filter(product=instance).count()
        count = instance.comments.count()
        return count


    def get_is_liked(self,instance):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        all_likes = instance.users_like.all()
        if user in all_likes:
            return True
        return False

    def get_product_images(self, instance):
        # image = Image.objects.filter(product=instance, is_primary= True ).first()
        image = instance.product_images.filter(is_primary = True).first()
        request = self.context.get('request')
        if image:
            image_url = image.image.url
            return request.build_absolute_uri(image_url)

        return None

    def get_all_image(self, instance):
        images = instance.product_images.all()
        all_image = []
        request = self.context.get('request')
        for image in images:
            all_image.append(request.build_absolute_uri(image.image.url))
        return all_image

    class Meta:
        model = Product
        # fields = ['id', 'product_name', 'slug', 'discount', 'price', 'rating', 'product_images']
        # fields = '__all__'
        exclude = ('users_like',)
        extra_fields = ['category_name','all_images','atribut','comment']




class CatalogModelSerialize(serializers.ModelSerializer):
    product = ProductSerialize(many=True,read_only=True)

    class Meta:
        model = Catalog
        # fields = ['id','catalog_name', 'product']
        fields = ['id', 'created_at','updated_at','catalog_name','slug','product']
        # exclude = ['products',]


class CategoryModelSerializers(serializers.ModelSerializer):

    category_image = serializers.SerializerMethodField(method_name='image')
    def image(self, instance):
        image = Image.objects.filter(category=instance, is_primary=True).first()
        request = self.context.get('request')
        if image:
            image_url = image.image.url
            return request.build_absolute_uri(image_url)
        return None
    class Meta:
        model = Category
        fields = '__all__'


class UserLoginSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username","password" ]

class UserRegisterSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField()
    # first_name = serializers.CharField()
    # last_name = serializers.CharField()
    # email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        # fields = ["id", "username", "first_name",
        #           "last_name", "email", "password", "password2"]
        fields = ["id", "username","password", "password2"]
        extra_kwargs = {
            'password': {"write_only": True}
        }

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            detail = {
                "detail": "User Already exist!"
            }
            raise ValidationError(detail=detail)
        return username

    def validate(self, instance):
        if instance['password'] != instance['password2']:
            raise ValidationError({"message": "Both password must match"})

        # if User.objects.filter(email=instance['email']).exists():
        #     raise ValidationError({"message": "Email already taken!"})

        return instance

    def create(self, validated_data):
        passowrd = validated_data.pop('password')
        passowrd2 = validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        user.set_password(passowrd)
        user.save()
        Token.objects.create(user=user)
        return user

class ProductSerializeDetail(serializers.ModelSerializer):
    category = serializers.CharField(source='category.category_name', read_only=True)
    product_images = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()

    def get_avg_rating(self,obj):
        avg_rating = obj.comments.aggregate(avg_rating=Round(Avg('reting')))
        if avg_rating.get('avg_rating'):
            return avg_rating.get('avg_rating')
        else:
            return 0

    def get_is_liked(self,instance):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        all_likes = instance.users_like.all()
        if user in all_likes:
            return True
        return False

    def get_product_images(self, instance):
        # image = Image.objects.filter(product=instance, is_primary= True ).first()
        image = instance.product_images.filter(is_primary = True).first()
        request = self.context.get('request')
        if image:
            image_url = image.image.url
            return request.build_absolute_uri(image_url)

        return None
    class Meta:
        model = Product
        # fields = ['id', 'product_name', 'slug', 'discount', 'price', 'rating', 'product_images']
        fields = '__all__'



class CategoryModelSerializersDetail(serializers.ModelSerializer):
    product = ProductSerializeDetail(many=True,read_only=True)
    class Meta:
        model = Category
        fields = ['category_name','product',]

class ProductAtriburSerializer(serializers.ModelSerializer):
    product = ProductSerialize(many=True,read_only=True)
    key = AtributSerializer(many=True, read_only=True)
    value = AtributValueSerializer(many=True, read_only=True)

    class Meta:
        model = PraductAttribute
        fields = ['id','product','key','value','pk']



