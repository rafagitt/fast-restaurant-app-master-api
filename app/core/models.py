import uuid
import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings


def food_image_file_path(instance, file_name):
    """Generate file path"""
    ext = file_name.split('.')[-1]
    file_name = f'{uuid.uuid4()}.{ext}'
    return os.path.join('uploads/food/', file_name)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Creating a superuser"""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Customer user model that support using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    creation_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=True
    )
    objects = UserManager()
    USERNAME_FIELD = 'email'


# Foods and orders starts from here

class Food(models.Model):
    """Food object"""
    name = models.CharField(max_length=255)
    time_order_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(null=True, upload_to=food_image_file_path)

    def __str__(self):
        return self.name


class Order(models.Model):
    """Food Orders"""
    food = models.ForeignKey('Food', on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    creation_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=True
    )
    subtotal = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    discount = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    total = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    completed = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)

    def __str__(self):
        return f'Food Order: {self.food}, Client: {self.user}'
