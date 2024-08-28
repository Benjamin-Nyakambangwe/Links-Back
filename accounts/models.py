from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone



class UserAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, user_type, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, user_type=user_type, **extra_fields)
        
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, first_name, last_name, user_type, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, first_name, last_name, user_type, password, **extra_fields)

class UserAccount(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('publisher', 'Publisher'),
        ('advertiser', 'Advertiser'),
    )
    
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='publisher')
    date_joined = models.DateTimeField(auto_now_add=True, null=True)
    last_login = models.DateTimeField(auto_now=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_type']

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name


    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email
    


class PublisherProfile(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name='publisher_profile')
    phone = models.CharField(max_length=50)

    def __str__(self):
        return self.user.email




class AdvertiserProfile(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name='advertiser_profile')
    phone = models.CharField(max_length=50)

    def __str__(self):
        return self.user.email





@receiver(post_save, sender=UserAccount)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'publisher':
            PublisherProfile.objects.create(user=instance)
        elif instance.user_type == 'advertiser':
            AdvertiserProfile.objects.create(user=instance)

@receiver(post_save, sender=UserAccount)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 'pulisher':
        instance.publisher_profile.save()
    elif instance.user_type == 'advertiser':
        instance.advertiser_profile.save()

