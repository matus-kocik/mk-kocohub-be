from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Custom manager for User model that uses email as the unique identifier
    instead of username.

    This manager handles the creation of both regular users and superusers,
    ensuring proper email validation and password handling.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a new user with the given email and password.

        Args:
            email (str): User's email address (required)
            password (str, optional): User's password
            **extra_fields: Additional fields to be saved on the user model

        Returns:
            CustomUser: Created user instance

        Raises:
            ValueError: If email is not provided
        """
        if not email:
            raise ValueError("The Email field is required and must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a new superuser with the given email and password.
        Extra fields are added to indicate that the user is staff, active,
        and indeed a superuser.

        Args:
            email (str): Superuser's email address (required)
            password (str, optional): Superuser's password
            **extra_fields: Additional fields to be saved on the user model

        Returns:
            CustomUser: Created superuser instance with admin privileges
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses email as the username field.

    This model extends Django's AbstractBaseUser and PermissionsMixin to create
    a fully featured user model with admin-compliant permissions.

    Attributes:
        email (EmailField): User's email address (unique identifier)
        first_name (CharField): User's first name
        last_name (CharField): User's last name
        is_active (BooleanField): Whether this user account is active
        is_staff (BooleanField): Whether this user can access the admin site
        date_joined (DateTimeField): When this user account was created
    """

    email = models.EmailField(
        unique=True, verbose_name="email address", help_text="User's email address"
    )
    first_name = models.CharField(
        max_length=32, verbose_name="first name", help_text="User's first name"
    )
    last_name = models.CharField(
        max_length=32, verbose_name="last name", help_text="User's last name"
    )
    is_active = models.BooleanField(
        default=True, help_text="User's account status", verbose_name="active"
    )
    is_staff = models.BooleanField(
        default=False, help_text="User's staff status", verbose_name="staff"
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="date joined",
        help_text="User's registration date",
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
