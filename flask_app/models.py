# accounts/models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.conf import settings


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)  # This hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
class Specials(models.Model):
    ProductName = models.CharField(max_length=255)
    ProductNameType = models.CharField(max_length=255)  # For broader matching
    ProductPrice = models.DecimalField(max_digits=10, decimal_places=2)
    # ... other fields as needed ...

    def __str__(self):
        return f"{self.ProductName} ({self.ProductNameType}) - ${self.ProductPrice}"


from django.db import models

class RankedProductPricess(models.Model):
    ProductNameType = models.CharField(max_length=255)
    ProductPrice = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.IntegerField()
    recipe_id = models.AutoField(primary_key=True) # Add the missing recipe_id field

    class Meta:
        managed = False
        db_table = 'rankedprices'

from django.contrib.auth.models import User

class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Foreign key to User model
    DishName = models.CharField(max_length=255)
    DishType = models.CharField(max_length=255)
    DishSort = models.CharField(max_length=255)
    DishTime = models.CharField(max_length=255)
    ProductOtherProducts = models.TextField()
    Description = models.TextField()
    Machinery = models.TextField()

    def __str__(self):
        return self.DishName
class Account(AbstractBaseUser):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
