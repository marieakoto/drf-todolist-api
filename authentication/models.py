from django.db import models
from helpers.models import TrackingModel
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import (PermissionsMixin, UserManager, AbstractBaseUser)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.apps import apps
import jwt
from django.conf import settings
from datetime import datetime,timedelta
from authentication.exceptions import validate_email, validate_superuser_fields,validate_username,validate_user_fields



class MyUserManager(UserManager):         ##This manager is going to provide methods for creating regular users and superusers.Allows to customize how queries are performed on the model.

    def _create_user(self, username, email, password, **extra_fields):        
        validate_username(username)
        validate_email(email)
        
        email = self.normalize_email(email)                         
        
        GlobalUserModel = apps.get_model(                                       
            self.model._meta.app_label, self.model._meta.object_name
        )

        username = GlobalUserModel.normalize_username(username)              

        user = self.model(username=username, email=email, **extra_fields)

        user.password = make_password(password)                 
        user.save(using=self._db)                               
        return user

    def create_user(self, username, email, password=None, **extra_fields):        
        extra_fields.setdefault("is_staff", False)                                 
        extra_fields.setdefault("is_superuser", False)                               
       
        validate_username(username)
        validate_email(email)
        validate_user_fields(extra_fields)

        return self._create_user(username, email, password, **extra_fields)         

    def create_superuser(self, username, email, password=None, **extra_fields):         
        extra_fields.setdefault("is_staff", True)                                     
        extra_fields.setdefault("is_superuser", True) 

        validate_username(username)
        validate_email(email)
        validate_superuser_fields(extra_fields)

        return self._create_user(username, email, password, **extra_fields)              
    


class User(AbstractBaseUser, PermissionsMixin,TrackingModel):               #An abstract base class implementing a fully featured User model with admin-compliant permissions.
    
    username_validator = UnicodeUsernameValidator()         #Ennsures that usernames adhere to certain criteria

    username = models.CharField(_("username"), max_length=150, unique=True,        #Defines the username field and validates it with the username validator
                                
        help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        validators=[username_validator],
        error_messages={"unique": _("A user with that username already exists."),},
    )

    email = models.EmailField(_("email address"), blank=False, unique = True)

    is_staff = models.BooleanField(_("staff status"), default=False,
        help_text=_("Designates whether the user can log into this admin site."),   #Indicates whether the user is a staff member
    )

    is_active = models.BooleanField(_("active"), default=True,              
        help_text=_("Designates whether this user should be treated as active. " ),        #Indicates whether this user is active
    )

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)       #Stores the date and the time the user was created.Uses the default value of the current time

    email_verified =  models.BooleanField(_("email_verified"), default=False,
        help_text=_("Designates whether this user's email is verified."),               #Indicates whether this user's email has been verified 
    )

    objects = MyUserManager()      #Insists that instances of the User class should be managed by the MyUserManger earlier defined


    EMAIL_FIELD = "email"          #Specifies which fields to be used for authentication.In this case email is the primary identifier
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property                    ##To generate access tokens when needed.
    def token(self):
        token = jwt.encode({'username': self.username, 'email': self.email, 
                            'exp': datetime.utcnow() + timedelta(hours=24)},
                               settings.SECRET_KEY, algorithm='HS256')
    
        return token
    