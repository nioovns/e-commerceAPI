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
        
    