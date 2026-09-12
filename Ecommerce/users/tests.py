from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User

class RegisterTestCase(APITestCase):

    def test_register_success(self):
        data = {
            "first_name": "amir",
            "last_name": "amiri",
            "email": "amir@example.com",
            "phone_number": "09123456789",
            "address": "yazd",
            "password": "testpassword123",
        }

        response = self.client.post(
            reverse("register"),
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            User.objects.filter(
                email="amir@example.com"
            ).exists()
        )
    
    def test_first_name_too_short(self):
        data = {
            "first_name": "a",
            "last_name": "amiri",
            "email": "amir@example.com",
            "phone_number": "09123456789",
            "address": "yazd",
            "password": "testpassword123",
        }

        response = self.client.post(
            reverse("register"),
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertIn(
            "first_name",
            response.data
        )
    
    def test_first_name_contains_number(self):
        data = {
            "first_name": "amir2",
            "last_name": "amiri",
            "email": "amir@example.com",
            "phone_number": "09123456789",
            "address": "yazd",
            "password": "testpassword123",
        }

        response = self.client.post(
            reverse("register"),
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertIn(
            "first_name",
            response.data
        )
            
    def test_phone_number_without_zero(self):
        data = {
            "first_name": "amir",
            "last_name": "amiri",
            "email": "amir@example.com",
            "phone_number": "9123456789",
            "address": "yazd",
            "password": "testpassword123",
        }
        response = self.client.post(
            reverse("register"),
            data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertIn(
            "phone_number",
            response.data
        )
    
    def test_phone_number_too_short(self):
        data = {
            "first_name": "amir",
            "last_name": "amiri",
            "email": "amir@example.com",
            "phone_number": "091234567",
            "address": "yazd",
            "password": "testpassword123",
        }

        response = self.client.post(
            reverse("register"),
            data
        )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertIn(
            "phone_number",
            response.data
        )

    def test_duplicate_email(self):
        data = {
            "first_name": "amir",
            "last_name": "amiri",
            "email": "amir@example.com",
            "phone_number": "09123456789",
            "address": "yazd",
            "password": "testpassword123",
        }

        response = self.client.post(
            reverse("register"),
            data
        )
        
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        
        
        data2 = {
            "first_name": "amin",
            "last_name": "amini",
            "email": "amir@example.com",
            "phone_number": "09123456788",
            "address": "tehran",
            "password": "testpassword123",
        }

        response2 = self.client.post(
            reverse("register"),
            data2
        )
 
        self.assertEqual(
            response2.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertIn(
            "email",
            response2.data
        )       
 
    def test_password_too_short(self):
        data = {
            "first_name": "amir",
            "last_name": "amiri",
            "email": "amir@example.com",
            "phone_number": "09123456789",
            "address": "yazd",
            "password": "testp",
        }

        response = self.client.post(
            reverse("register"),
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertIn(
            "password",
            response.data
        )

    def test_password_not_returned(self):       
        data = {
            "first_name": "amir",
            "last_name": "amiri",
            "email": "amir@example.com",
            "phone_number": "09123456789",
            "address": "yazd",
            "password": "testpassword123",
        }

        response = self.client.post(
            reverse("register"),
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertNotIn(
            "password",
            response.data
        )

    def test_password_is_hashed(self):
        data = {
            "first_name": "amir",
            "last_name": "amiri",
            "email": "amir@example.com",
            "phone_number": "09123456789",
            "address": "yazd",
            "password": "testpassword123",
        }

        response = self.client.post(
            reverse("register"),
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        user = User.objects.get(
            email="amir@example.com"
        )

        self.assertNotEqual(
            user.password,
            "testpassword123"
        )

        self.assertTrue(
            user.check_password("testpassword123")
        )