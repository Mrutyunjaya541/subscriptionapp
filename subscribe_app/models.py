from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db.models import base
from rest_framework.serializers import BaseSerializer, ModelSerializer


class UserManager(BaseUserManager):
    def create_user(self, email, first_name,last_name,dob,address,company,password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        
        if not first_name:
            raise ValueError('User must have first_name')
        
        if not last_name:
            raise ValueError('User must have last_name')
        
        if not dob:
            raise ValueError('User must have dob')
        
        if not address:
            raise ValueError('User must have address')

        if not company:
            raise ValueError('User must have Company')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.first_name = first_name
        user.last_name  = last_name
        user.dob = dob
        user.address = address
        user.company = company
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email,first_name,last_name,dob, address,company,password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            dob,
            address,
            company,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email,first_name,last_name,dob, address,company, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            dob,
            address,
            company,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=264)
    last_name = models.CharField(max_length=100)
    address = models.TextField()
    dob = models.DateField(max_length=8)
    company = models.CharField(max_length=264)
    is_active = models.BooleanField(default=True)
    is_manager = models.BooleanField(default=False)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser

    objects = UserManager()
    # notice the absence of a "Password field", that is built in
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','dob','address','company'] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin
class Subscribe_Plan(models.Model):
    amount = models.FloatField()
    subscibe_plan = models.CharField(max_length=164)


    def __str__(self) -> str:
        return self.subscibe_plan

class User_Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    sub_plan = models.ForeignKey(Subscribe_Plan,on_delete=models.CASCADE)
    is_subscribed = models.BooleanField(default=False)
    subscribe_date = models.DateTimeField(blank=True,null=True)
    cancel_date = models.DateTimeField(null=True,blank=True)
    expiry_date = models.DateTimeField(null=True,blank=True)
    is_cancel = models.BooleanField(default=False)
    left_day = models.IntegerField(blank=True,null=True)
    order_id = models.CharField(max_length=364,blank=True,null=True)


    def __str__(self) -> str:
        return self.user.first_name



class Razorpay_Detail(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_id = models.CharField(unique=True,max_length=264)
    success_status = models.BooleanField(default=False)
    amount = models.CharField(max_length=265,blank=True,null=True)


