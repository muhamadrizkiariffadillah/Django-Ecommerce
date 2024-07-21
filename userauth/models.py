from django.db import models
from django.contrib.auth.models import AbstractUser
from shortuuid.django_fields import ShortUUIDField


# Create your models here.

class User(AbstractUser):
    """Custom user model extending AbstractUser."""

    username = models.CharField(unique=True, max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def save_user(self, *args, **kwargs):
        """
            Custom save method for User model.

            This method automatically populates full_name and username fields
            if they are not provided:
                - If full_name is empty or None, it defaults to the username part of the email.
                - If username is empty or None, it defaults to the username part of the email.

            Args:
                *args: Additional positional arguments.
                **kwargs: Additional keyword arguments.

            Returns:
                None
        """
        email_username = self.email.split("@")

        if not self.full_name:
            self.full_name = email_username

        if not self.username:
            self.username = email_username

        super(User, self).save(*args, **kwargs)


class UsersProfile(models.Model):
    """
    Model representing user profile information.

    Attributes:
        pid (ShortUUIDField): Unique identifier for the profile.
        user (User): The user associated with this profile.
        full_name (str): The full name of the user (optional).
        image (ImageField): Profile picture of the user (optional).
        about (str): A brief description or bio of the user (optional).
        gender (str): Gender of the user (optional).
        country (str): Country of residence of the user (optional).
        state (str): State or region of residence of the user (optional).
        city (str): City of residence of the user (optional).
        address (str): Detailed address of the user (optional).
        date (DateField): Date when the profile was created.

    Methods:
        __str__(): Returns a string representation of the profile.
        save(*args, **kwargs): Custom save method to populate `full_name` from `user` if not provided.
    """
    pid = ShortUUIDField(unique=True, length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='media', blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        """
            String representation of the user profile.

            Returns:
                str: Full name if available, otherwise falls back to the user's full name.
        """
        if self.full_name:
            return str(self.full_name)
        else:
            return str(self.user.full_name)

    def save(self, *args, **kwargs):
        """
            Save method for the user profile.
            If `full_name` is not provided, it populates it from the associated `user`.

            Args:
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.
        """
        if not self.full_name:
            self.full_name = self.user.full_name

        super(UsersProfile, self).save(*args, **kwargs)

