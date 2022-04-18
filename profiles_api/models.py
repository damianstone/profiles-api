from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

# Create your models here.

# MODESL WE NEED FOR TOOGETHER

# 1- create user 
# 2 - create a group profile 

# manager is the way we check the input values in somehow
class UserProfileManager(BaseUserManager):
    # manager for user profiles
    
    def create_user(self, email, name, password=None):
        # create a new user profile
        if not email:
            # message error that user can see 
            raise ValueError('put an email aweonao')
        
        # make the email in capital letters
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        
        # converter to a hash 
        user.set_password(password)
        # save in the django db
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, name, password):
        # create and save a new superuser with given details
        user = self.create_user(email, name, password)
        
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        
        return user
        


# create the model (same as the dummy models in JS)
# class representation always in singular
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system."""
    email= models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    # manager to get django know how to use this model
    objects = UserProfileManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    def get_full_name(self): 
        # retrieve full name of user
        return self.name
    
    def get_short_name(self):
        # return short name of user
        return self.name
    
    def __str__(self):
        # what u see when u open the profiles users in the admin panel
        return self.email


# profile status updates
class ProfileFeedItem(models.Model):
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True) # add the date time when its created
    
    # return the entire model as a string
    def __str__(self):
        return self.status_text
    
