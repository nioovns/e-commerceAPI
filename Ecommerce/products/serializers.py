from rest_framework import serializers
from .models import Product, Category, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "category_name",
        ]    
    
    def validate_category_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Category name must have at least 2 characters."
            )
        return value
        
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            "id",
            "product",
            "image",
            "is_primary",
            "created_at",
        ]
    
    def validate(self, attrs):
        if attrs.get("is_primary"):
            product = attrs["product"]

            if ProductImage.objects.filter(
                product=product,
                is_primary=True
            ).exists():
                raise serializers.ValidationError(
                    "This product already has a primary image."
                )

        return attrs
        
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True
    )

    images = ProductImageSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "stock",
            "category",
            "category_id",
            "images",
            "created_at",
            "updated_at",
            "is_active",
        ]
        
    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Product name must have at least 2 characters."
            )
        return value
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than zero."
            )
        return value
        
        
class ProductImageUploadSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )

    image = serializers.ImageField()

    is_primary = serializers.BooleanField(
        required=False,
        default=False
    )