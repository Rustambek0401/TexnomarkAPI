
from django.contrib import admin
from django.urls import path,include
from texnomark.views import (CategoryListView,
                             CatalogListView,
                             ProductListView,
                             ImagelistView,
                             CommentListView,
                             ProductAtributListView,
                             # AddressListView,
                            Atribut_key,
                            Atribot_Value
                             )
from texnomark import views
from texnomark.auth import (UserLoginAPIView,
                            UserRegisterAPIView,
                            UserLogoutAPIView)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('category',views.CategoryModelViewSet,basename='category'),
router.register('catalog',views.CatalogModelViewSet,basename='group')
router.register('product',views.ProductModelViewSet,basename='product')
router.register('key',views.Atribut_key_ModelViewSet,basename='key')
router.register('value',views.Atribut_value_ModelViewSet,basename='value')

urlpatterns = [
    path('router',include(router.urls)),
    path('',ProductListView.as_view(), name='all_product'),
    path('categories/', CategoryListView.as_view(),name='index'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='detail'),

    path('catalog/', CatalogListView.as_view(),name='catalog'),
    path('product/', ProductListView.as_view(),name='product'),
    path('image/', ImagelistView.as_view(),name='image'),
    path('comment/', CommentListView.as_view(),name='comment'),
    path('atribut/', ProductAtributListView.as_view(),name='atribut'),
    path('key/', Atribut_key.as_view(),name='key'),
    path('value/', Atribot_Value.as_view(),name='value'),
    # path('address/', AddressListView.as_view(),name='address'),

#                           """ CRUD """

    path('Crud_category/', views.CategitiyListCrud.as_view(),name='CRUD_category'),
    path('Crud_product/', views.ProductList_Crud.as_view(),name='CRUD_product'),
    path('Crud_catalog/', views.CatalogListCrud.as_view(),name='CRUD_catalog'),
    path('Crud_detail_category/<int:pk>', views.CategoryDetialCrud.as_view(),name='detail_category'),
    path('Crud_detail_product/<int:pk>', views.ProductDetail.as_view(),name='detail_product'),
  # ADD
    path('add_category/', views.CategoryAddCrud.as_view(),name='CRUD_Add_Category'),
    path('add_catalog/', views.CatalogAddCrud.as_view(),name='CRUD_Add_Catalog'),
    path('add_product/', views.ProductAddCrud.as_view(),name='CRUD_Add_Product'),
  # Updata
    path('Categoty_Updata/<slug:slug>',views.CategoryUpdata.as_view(),name='Categoty_Updata'),
    path('Catalog_Updata/<int:pk>',views.CatalogUpdata.as_view(),name='Catalog_Updata'),
    path('Product_Updata/<int:pk>',views.ProductUpdata.as_view(),name='Product_Updata'),
   #delete
    path('category_delete/<slug:slug>',views.CategoryDelete.as_view(),name='category_delete'),
    path('catalog_delete/<int:pk>',views.CatalogDelete.as_view(),name='catalog_delete'),
    path('product_delete/<int:pk>',views.ProductDelete.as_view(),name='product_delete'),


#                              LOGIN
    path('login/', UserLoginAPIView.as_view(),name='login'),
    path('register/',UserRegisterAPIView.as_view(),name='register'),
    path('logout/', UserLogoutAPIView.as_view(),name='logout'),

]
