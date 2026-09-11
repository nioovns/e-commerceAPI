import re
from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "address",
            "password",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        return user
    
    
    def validate_phone_number(self, phone_number):
        if not re.fullmatch(r"09\d{9}", phone_number):
            raise serializers.ValidationError(
                "Phone number must be 11 digits and start with 09."
            )
        return phone_number
    
    def validate_first_name(self, value):
        name = value.replace(" ", "")
        
        if not name.isalpha():
            raise serializers.ValidationError(
                "First name must contain only letters."
            )
            
        if len(name) < 3:
            raise serializers.ValidationError(
                "First name must have at least 3 letters."
            )
            
        return value
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]

        user = authenticate(
            username=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "This account is inactive."
            )

        attrs["user"] = user

        return attrs

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "address",
        ]
        read_only_fields = ["id", "email"]