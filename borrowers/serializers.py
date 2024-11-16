from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import Borrower
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_admin'] = user.is_staff
        token['is_borrower'] = user.is_borrower
        return token

class BorrowerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)  # تغییر به write_only
    email = serializers.EmailField(write_only=True)    # تغییر به write_only
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Borrower
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        # استخراج اطلاعات کاربر
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        # ایجاد کاربر جدید
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # ایجاد Borrower با کاربر مرتبط
        return Borrower.objects.create(user=user, **validated_data)
