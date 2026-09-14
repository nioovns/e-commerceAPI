from django.urls import path

from .views import (
    ProductView,
    ProductDetailView,
    CategoryView,
    ProductImageView,
    CategoryDetailView,
    ProductImageDetailView,
)


urlpatterns = [

    path(
        "products/",
        ProductView.as_view(),
        name="products"
    ),

    path(
        "products/<int:pk>/",
        ProductDetailView.as_view(),
        name="product-detail"
    ),

    path(
        "categories/",
        CategoryView.as_view(),
        name="categories"
    ),
    path(
        "categories/<int:pk>/",
        CategoryDetailView.as_view(),
        name="category-detail"
    ),
    path(
        "product-images/",
        ProductImageView.as_view(),
        name="product-images"
    ),
        path(
        "product-images/<int:pk>/",
        ProductImageDetailView.as_view(),
        name="product-images-detail"
    ),

]