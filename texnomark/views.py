from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from texnomark.models import (Category,
                              Catalog,
                              Product,
                              Image,
                              Comment,
                              PraductAttribute,
                              Address,
                              Attribute,
                              AttributeValue)
from texnomark.serializers import (CategoryModelSerializers,
                               CatalogModelSerialize,
                               ProductSerialize,
                               ImageSerializer,
                                CommentSerializer,
                                ProductAtriburSerializer,
                                AddressSerializer,
                                CategoryModelSerializersDetail,
                                AtributSerializer,
                                AtributValueSerializer,
                               )
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
class AddressListView(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        addres = Address.objects.all()
        serializer = AddressSerializer(addres,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductAtributListView(APIView):

    def get(self, request):
        atribut = PraductAttribute.objects.all()
        serializer = ProductAtriburSerializer(atribut,many=True, context={'request':request})
        return Response(serializer.data,status=status.HTTP_200_OK)


class CategoryListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CategoryModelSerializers
    queryset = Category.objects.all()
    @method_decorator(cache_page(5))
    def get(self, *args, **kwargs):
        return super().get(*args,**kwargs)

class CatalogListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CatalogModelSerialize
    queryset = Catalog.objects.all()
    @method_decorator(cache_page(60*30))
    def get(self, *args, **kwargs):
        return super().get(*args,**kwargs)

class CategoryDetailView(APIView):
    def get(self,request, slug):
        category = get_object_or_404(Category, slug=slug)
        serializers = CategoryModelSerializersDetail(category,context={'request':request})
        return Response(serializers.data, status=status.HTTP_200_OK)


class ProductListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = ProductSerialize
    queryset = Product.objects.all()
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['category', 'in_stock']

    @method_decorator(cache_page(60*30))
    def get(self, *args, **kwargs):
        return super().get(*args,**kwargs)


    def get_queryset(self):
        queryset = Product.objects.select_related('category').prefetch_related('product')
        return queryset

class ImagelistView(APIView):
    def get(self, request):
        image = Image.objects.all()
        serializers = ImageSerializer(image,many=True, context={'request':request})
        return Response(serializers.data, status=status.HTTP_200_OK)
class CommentListView(APIView):
    def get(self,request):
        comment = Comment.objects.all()
        serializer = CommentSerializer(comment,many=True,context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class Atribut_key(generics.ListAPIView):
    model = Attribute
    serializer_class = AtributSerializer
    queryset = Attribute.objects.all()

class Atribot_Value(generics.ListAPIView):
    model = AttributeValue
    serializer_class = AtributValueSerializer
    queryset = AttributeValue.objects.all()

""" CRUD """


class CategitiyListCrud(generics.ListAPIView):
    model = Category
    serializer_class = CategoryModelSerializers
    queryset = Category.objects.all()

class ProductList_Crud(generics.ListAPIView):
    model = Product
    serializer_class = ProductSerialize
    queryset = Product.objects.all()

class CatalogListCrud(generics.ListAPIView):
    model = Catalog
    serializer_class = CatalogModelSerialize
    queryset = Catalog.objects.all()


class CategoryDetialCrud(generics.RetrieveAPIView):
    model = Category
    serializer_class = CategoryModelSerializers
    lookup_field = 'pk'
    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset
class ProductDetail(generics.RetrieveAPIView):
    model = Product
    serializer_class = ProductSerialize
    lookup_field = 'pk'
    def get_queryset(self):
        queryset = Product.objects.all()
        return queryset

class CategoryAddCrud(generics.CreateAPIView):
    serializer_class = CategoryModelSerializers
    queryset = Category.objects.all()

class CatalogAddCrud(generics.CreateAPIView):
    serializer_class = CatalogModelSerialize
    queryset = Catalog.objects.all()

class ProductAddCrud(generics.CreateAPIView):
    serializer_class = ProductSerialize
    queryset = Product.objects.all()

class CategoryUpdata(generics.UpdateAPIView):
    serializer_class = CategoryModelSerializers
    queryset = Category.objects.all()
    lookup_field = 'slug'

class CatalogUpdata(generics.UpdateAPIView):
    serializer_class = CatalogModelSerialize
    queryset = Catalog.objects.all()
    lookup_field = 'pk'

class ProductUpdata(generics.UpdateAPIView):
    serializer_class = ProductSerialize
    queryset = Product.objects.all()
    lookup_field = 'pk'

class CategoryDelete(generics.DestroyAPIView):
    serializer_class = CategoryModelSerializers
    lookup_field = 'slug'
    queryset = Category.objects.all()

class CatalogDelete(generics.DestroyAPIView):
    serializer_class = CatalogModelSerialize
    lookup_field = 'pk'
    queryset = Catalog.objects.all()

class ProductDelete(generics.DestroyAPIView):
    serializer_class = ProductSerialize
    lookup_field = 'pk'
    queryset = Product.objects.all()

# """" ModelViewSet """
class CategoryModelViewSet(viewsets.ModelViewSet):
    serializer_class = CategoryModelSerializers
    queryset = Category.objects.all()
    lookup_field = 'pk'

class CatalogModelViewSet(viewsets.ModelViewSet):
    serializer_class = CatalogModelSerialize
    queryset = Catalog.objects.all()
    lookup_field = 'pk'

class ProductModelViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerialize
    queryset = Product.objects.all()
    lookup_field = 'pk'

class Atribut_key_ModelViewSet(viewsets.ModelViewSet):
    serializer_class = AtributSerializer
    queryset = Attribute.objects.all()
    lookup_field = 'pk'

class Atribut_value_ModelViewSet(viewsets.ModelViewSet):
    serializer_class = AtributValueSerializer
    queryset = AttributeValue.objects.all()
    lookup_field = 'pk'

class Atribut_key_value_ModelViewSet(viewsets.ModelViewSet):
    serializer_class = ProductAtriburSerializer
    queryset = PraductAttribute.objects.all()
    lookup_field = 'pk'
