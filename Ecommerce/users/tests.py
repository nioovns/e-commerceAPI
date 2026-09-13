from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

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
        

class LoginTestCase(APITestCase):

    def test_login_success(self):
        User.objects.create_user(
            email="amir@example.com",
            phone_number="09123456789",
            password="testpassword123"
        )

        data = {
            "email": "amir@example.com",
            "password": "testpassword123"
        }

        response = self.client.post(
            reverse("login"),
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIn(
            "access",
            response.data
        )

        self.assertIn(
            "refresh",
            response.data
        )

    def test_login_wrong_email(self):
        User.objects.create_user(
            email="amir@example.com",
            phone_number="09123456789",
            password="testpassword123"
        )

        data = {
            "email": "amirmm@example.com",
            "password": "testpassword123"
        }

        response = self.client.post(
            reverse("login"),
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertNotIn(
            "access",
            response.data
        )

        self.assertNotIn(
            "refresh",
            response.data
        )
               
    def test_login_wrong_password(self):
        User.objects.create_user(
            email="amir@example.com",
            phone_number="09123456789",
            password="testpassword123"
        )

        data = {
            "email": "amir@example.com",
            "password": "testpassword1234"
        }

        response = self.client.post(
            reverse("login"),
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        
        self.assertNotIn(
            "access",
            response.data
        )

        self.assertNotIn(
            "refresh",
            response.data
        )
    
    def test_login_inactive_user(self):
        User.objects.create_user(
            email="amir@example.com",
            phone_number="09123456789",
            password="testpassword123"
        )
        user = User.objects.get(
            email="amir@example.com"
        )
        user.is_active = False
        user.save()
        
        data = {
            "email": "amir@example.com",
            "password": "testpassword123"
        }

        response = self.client.post(
            reverse("login"),
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        
        self.assertNotIn(
            "access",
            response.data
        )

        self.assertNotIn(
            "refresh",
            response.data
        )
        
    def test_login_without_email(self):
        User.objects.create_user(
            email="amir@example.com",
            phone_number="09123456789",
            password="testpassword123"
        )

        data = {
            "password": "testpassword1234"
        }

        response = self.client.post(
            reverse("login"),
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        
        self.assertNotIn(
            "access",
            response.data
        )

        self.assertNotIn(
            "refresh",
            response.data
        )
        
    def test_login_without_password(self):
        User.objects.create_user(
            email="amir@example.com",
            phone_number="09123456789",
            password="testpassword123"
        )

        data = {
            "email": "amir@example.com"
        }

        response = self.client.post(
            reverse("login"),
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        
        self.assertNotIn(
            "access",
            response.data
        )

        self.assertNotIn(
            "refresh",
            response.data
        )
        
    def test_login_token_is_valid(self):
        User.objects.create_user(
            email="amir@example.com",
            phone_number="09123456789",
            password="testpassword123"
        )

        data = {
            "email": "amir@example.com",
            "password": "testpassword123"
        }

        response = self.client.post(
            reverse("login"),
            data
        )

        access_token = response.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        profile_response = self.client.get(
            reverse("profile")
        )

        self.assertEqual(
            profile_response.status_code,
            status.HTTP_200_OK
        )
        
        
class ProfileTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="amir@example.com",
            phone_number="09123456789",
            password="testpassword123",
            first_name="amir",
            last_name="amiri",
            address="yazd"
        )
            
    def test_get_profile(self):
        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        response = self.client.get(
            reverse("profile")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["email"],
            "amir@example.com"
        )
    
    def test_get_profile_without_authentication(self):
        response = self.client.get(
            reverse("profile")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
        
    def test_update_profile(self):
        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        data = {
            "first_name": "ali",
            "last_name": "alavi",
            "phone_number": "09111111111",
            "address": "tehran"
        }

        response = self.client.put(
            reverse("profile"),
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["first_name"],
            "ali"
        )

        self.assertEqual(
            response.data["address"],
            "tehran"
        )
        
    def test_partial_update_profile(self):
        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        data = {
            "first_name": "ali",
        }

        response = self.client.patch(
            reverse("profile"),
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["first_name"],
            "ali"
        )

        self.assertEqual(
            response.data["last_name"],
            "amiri"
        )

    def test_email_cannot_be_updated(self):
        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        data = {
            "email": "ali@gmail.com"
        }

        response = self.client.patch(
            reverse("profile"),
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["email"],
            "amir@example.com"
        )

    def test_profile_returns_correct_user(self):
        another_user = User.objects.create_user(
            email="ali@example.com",
            phone_number="09111111111",
            password="testpassword123",
            first_name="ali",
            last_name="alavi"
        )

        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        response = self.client.get(
            reverse("profile")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["email"],
            self.user.email
        )

        self.assertNotEqual(
            response.data["email"],
            another_user.email
        )
