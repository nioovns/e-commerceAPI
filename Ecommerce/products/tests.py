from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Category, Product, ProductImage
from users.models import User


class CategoryAPITestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email="admin@test.com",
            password="Admin12345",
            phone_number="09123456789",
            is_staff=True
        )

        self.user = User.objects.create_user(
            email="user@test.com",
            password="User12345",
            phone_number="09987654321"
        )

        self.category = Category.objects.create(
            category_name="Shoes"
        )
    
    def test_category_list(self):
        response = self.client.get(
            reverse("categories")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
    
    
    def test_create_category_successful(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.post(
            reverse("categories"),
            {
                "category_name": "Laptops"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Category.objects.count(),
            2
        )    
    
    def test_create_category_unauthorized(self):
        response = self.client.post(
            reverse("categories"),
            {
                "category_name": "Laptops"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
    
    def test_create_category_by_user(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.post(
            reverse("categories"),
            {
                "category_name": "Laptops"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_create_category_with_invalid_name(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.post(
            reverse("categories"),
            {
                "category_name": "A"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        
    def test_create_category_duplicate_name(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.post(
            reverse("categories"),
            {
                "category_name": "clothes"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        
        response2 = self.client.post(
            reverse("categories"),
            {
                "category_name": "clothes"
            }
        )
        self.assertEqual(
            response2.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        
        
        
    def test_update_category_successful(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.post(
            reverse("categories"),
            {
                "category_name": "Laptops"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        category = Category.objects.get(
            category_name="Laptops"
        )

        response2 = self.client.patch(
            reverse(
                "category-detail",
                kwargs={"pk": category.id}
            ),
            {
                "category_name": "clothes"
            }
        )

        self.assertEqual(
            response2.status_code,
            status.HTTP_200_OK
        )

        category.refresh_from_db()

        self.assertEqual(
            category.category_name,
            "clothes"
        )
        
    def test_update_category_by_user(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.patch(
            reverse(
                "category-detail",
                kwargs={"pk": self.category.id}
            ),
            {
                "category_name": "Clothes"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
        
    def test_update_category_unauthorized(self):
        response = self.client.patch(
            reverse(
                "category-detail",
                kwargs={"pk": self.category.id}
            ),
            {
                "category_name": "Clock"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
        
    def test_update_category_with_invalid_name(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.post(
            reverse("categories"),
            {
                "category_name": "Laptops"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        category = Category.objects.get(
            category_name="Laptops"
        )

        response2 = self.client.patch(
            reverse(
                "category-detail",
                kwargs={"pk": category.id}
            ),
            {
                "category_name": "L"
            }
        )

        self.assertEqual(
            response2.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        
    def test_update_category_with_duplicate_name(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.post(
            reverse("categories"),
            {
                "category_name": "Laptops"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        category = Category.objects.get(
            category_name="Laptops"
        )

        response2 = self.client.patch(
            reverse(
                "category-detail",
                kwargs={"pk": category.id}
            ),
            {
                "category_name": "Shoes"
            }
        )

        self.assertEqual(
            response2.status_code,
            status.HTTP_400_BAD_REQUEST
        )
    
    
    def test_delete_category_successful(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.post(
            reverse("categories"),
            {
                "category_name": "Laptops"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        category = Category.objects.get(
            category_name="Laptops"
        )

        response2 = self.client.delete(
            reverse(
                "category-detail",
                kwargs={"pk": category.id}
            )
        )

        self.assertEqual(
            response2.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertFalse(
            Category.objects.filter(
                id=category.id
            ).exists()
        )

    def test_delete_category_by_user(self):
        self.client.force_authenticate(
            user=self.user
        )

        response2 = self.client.delete(
            reverse(
                "category-detail",
                kwargs={"pk": self.category.id}
            )
        )

        self.assertEqual(
            response2.status_code,
            status.HTTP_403_FORBIDDEN
        )
        
    def test_delete_category_unauthorized(self):
        response = self.client.delete(
            reverse(
                "category-detail",
                kwargs={"pk": self.category.id}
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
        

class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email="admin@test.com",
            password="Admin12345",
            phone_number="09123456789",
            is_staff=True
        )

        self.user = User.objects.create_user(
            email="user@test.com",
            password="User12345",
            phone_number="09987654321"
        )

        self.category = Category.objects.create(
            category_name="Shoes"
        )

        self.product = Product.objects.create(
            name="Nike Shoes",
            description="Running shoes",
            price=55000,
            stock=10,
            category=self.category
        )

    def test_product_list(self):
        response = self.client.get(
            reverse("products")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
    
    def test_product_detail(self):
        response = self.client.get(
            reverse(
                "product-detail",
                kwargs={"pk": self.product.id}
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["name"],
            "Nike Shoes"
        )

        self.assertEqual(
            response.data["stock"],
            10
        )
       
       
    def test_create_product_successful(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.post(
            reverse("products"),
            {
                "name": "Laptop",
                "description": "Gaming laptop",
                "price": 50000000,
                "stock": 5,
                "category_id": self.category.id
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Product.objects.count(),
            2
        )

        product = Product.objects.get(
            name="Laptop"
        )

        self.assertEqual(
            product.price,
            50000000
        )

        self.assertEqual(
            product.stock,
            5
        )

        self.assertEqual(
            product.category,
            self.category
        )
        
    def test_create_product_unauthorized(self):
        response = self.client.post(
            reverse("products"),
            {
                "name": "Laptop",
                "description": "Gaming laptop",
                "price": 50000000,
                "stock": 5,
                "category_id": self.category.id
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
        
    def test_create_product_by_user(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.post(
            reverse("products"),
            {
                "name": "Laptop",
                "description": "Gaming laptop",
                "price": 50000000,
                "stock": 5,
                "category_id": self.category.id
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
        
    def test_create_product_with_invalid_name(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.post(
            reverse("products"),
            {
                "name": "A",
                "description": "Gaming laptop",
                "price": 50000000,
                "stock": 5,
                "category_id": self.category.id
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        
    def test_create_product_without_name(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.post(
            reverse("products"),
            {
                "description": "Gaming laptop",
                "price": 50000000,
                "stock": 5,
                "category_id": self.category.id
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_create_product_with_invalid_price(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.post(
            reverse("products"),
            {
                "name": "Laptop",
                "description": "Gaming laptop",
                "price": 0,
                "stock": 5,
                "category_id": self.category.id
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        
    def test_create_product_with_negative_price(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.post(
            reverse("products"),
            {
                "name": "Laptop",
                "description": "Gaming laptop",
                "price": -5000,
                "stock": 5,
                "category_id": self.category.id
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        
    def test_create_product_with_negative_stock(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.post(
            reverse("products"),
            {
                "name": "Laptop",
                "description": "Gaming laptop",
                "price": 50000000,
                "stock": -5,
                "category_id": self.category.id
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        
    def test_create_product_with_invalid_category(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.post(
            reverse("products"),
            {
                "name": "Laptop",
                "description": "Gaming laptop",
                "price": 50000000,
                "stock": 5,
                "category_id": 9999
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        
    def test_create_product_without_description(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.post(
            reverse("products"),
            {
                "name": "Laptop",
                "price": 50000000,
                "stock": 5,
                "category_id": self.category.id
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        
        
    def test_update_product_successful(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.patch(
            reverse(
                "product-detail",
                kwargs={"pk": self.product.id}
            ),
            {
                "name": "Updated Shoes",
                "price": 75000,
                "stock": 20
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.name,
            "Updated Shoes"
        )

        self.assertEqual(
            self.product.price,
            75000
        )

        self.assertEqual(
            self.product.stock,
            20
        )
        
    def test_update_product_by_user(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.patch(
            reverse(
                "product-detail",
                kwargs={"pk": self.product.id}
            ),
            {
                "name": "Updated Shoes"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.name,
            "Nike Shoes"
        )
        
    def test_update_product_unauthorized(self):
        response = self.client.patch(
            reverse(
                "product-detail",
                kwargs={"pk": self.product.id}
            ),
            {
                "name": "Updated Shoes"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )   
        
    def test_update_product_with_invalid_name(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.patch(
            reverse(
                "product-detail",
                kwargs={"pk": self.product.id}
            ),
            {
                "name": "A"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.name,
            "Nike Shoes"
        )

    def test_update_product_with_invalid_price(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.patch(
            reverse(
                "product-detail",
                kwargs={"pk": self.product.id}
            ),
            {
                "price": 0
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.price,
            55000
        )

    def test_update_product_with_negative_price(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.patch(
            reverse(
                "product-detail",
                kwargs={"pk": self.product.id}
            ),
            {
                "price": -5000
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.price,
            55000
        )

    def test_update_product_with_negative_stock(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.patch(
            reverse(
                "product-detail",
                kwargs={"pk": self.product.id}
            ),
            {
                "stock": -5
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.stock,
            10
        )

    def test_update_product_with_invalid_category(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.patch(
            reverse(
                "product-detail",
                kwargs={"pk": self.product.id}
            ),
            {
                "category_id": 9999
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.category,
            self.category
        )
        
        
    def test_delete_product_successful(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.delete(
            reverse(
                "product-detail",
                kwargs={"pk": self.product.id}
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Product.objects.filter(
                id=self.product.id
            ).exists()
        )

    def test_delete_product_by_user(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.delete(
            reverse(
                "product-detail",
                kwargs={"pk": self.product.id}
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertTrue(
            Product.objects.filter(
                id=self.product.id
            ).exists()
        )

    def test_delete_product_unauthorized(self):
        response = self.client.delete(
            reverse(
                "product-detail",
                kwargs={"pk": self.product.id}
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
        
    