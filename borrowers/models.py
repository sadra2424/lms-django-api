from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    is_borrower = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # نام مرتبط سفارشی
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_user_permissions',  # نام مرتبط سفارشی
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username


class Borrower(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="borrower_profile")
    registration_date = models.DateField(auto_now_add=True)
    max_borrow_limit = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.user.username

