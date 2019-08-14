from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,\
                                                        PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):
    """" create for extra field for extra variable you pass """
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new User"""
        # user = self.model(email=email, **extra_fields)
        if not email:
            raise ValueError("user must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        """"This is for supporting multiple database and save the user """
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    """Remember bracket """
    objects = UserManager()
    # """" set username field is email id """
    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient to be used in a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
