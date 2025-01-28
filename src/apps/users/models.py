from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.db.models.functions import Concat


class CustomUserManager(BaseUserManager):
    """
    Custom manager for User model that uses email as the unique identifier
    instead of username.

    This manager handles the creation of both regular users and superusers,
    ensuring proper email validation and password handling.
    """

    def create_user(self, email, password, **extra_fields):
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

    def create_superuser(self, email, password, **extra_fields):
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
        full_name (GeneratedField): User's full name (first name + last name)
        is_active (BooleanField): Whether this user account is active
        is_staff (BooleanField): Whether this user can access the admin site
        date_joined (DateTimeField): When this user account was created
    """

    email = models.EmailField(
        unique=True, verbose_name="email address", help_text="email address"
    )
    first_name = models.CharField(
        max_length=46, verbose_name="first name", help_text="first name"
    )
    last_name = models.CharField(
        max_length=46, verbose_name="last name", help_text="last name"
    )
    full_name = models.GeneratedField(
        expression=Concat(
            models.F("first_name"), models.Value(" "), models.F("last_name")
        ),
        output_field=models.CharField(
            max_length=92,
        ),
        db_persist=True,
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

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def clean(self):
        """
        Custom clean method for the CustomUser model.

        Ensures that the email address is normalized (domain part is lowercase),
        and calls the parent class's clean method to handle additional validations.

        Raises:
            ValidationError: If any custom validation fails.

        Normalization:
            - Converts the domain part of the email to lowercase while keeping
                the local part intact.
        """
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
