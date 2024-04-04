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



class MyUserManager(UserManager):         ##This manager is going to provide methods for creating regular users and superusers.Allows to customize how queries are performed on the model.

    def _create_user(self, username, email, password, **extra_fields):        ##Creates and saves the instance of a user with provided arguments

        if not username:                                                        ##To ensure that username and email are set if not raises a  Value error.
            raise ValueError("The given username must be set")
        
        if not email:
            raise ValueError("The given email must be set")
        
        email = self.normalize_email(email)                          #This normalises the email to ensure consistency(converting uppercase to lowercase)
        
        GlobalUserModel = apps.get_model(                                       # Used to handle model changes in migrations
            self.model._meta.app_label, self.model._meta.object_name
        )

        username = GlobalUserModel.normalize_username(username)              #Also normalises the username

        user = self.model(username=username, email=email, **extra_fields)

        user.password = make_password(password)                 #The password is hashed using the makepassword function for security
        user.save(using=self._db)                                #The user instance is saved into the database
        return user

    def create_user(self, username, email, password=None, **extra_fields):        ## A convenient method for creating regular users specifically
        extra_fields.setdefault("is_staff", False)                                  #Sets the is staff to is false if not specified explicitly.
        extra_fields.setdefault("is_superuser", False)                               #Sets the is superuser to is false if not specified explicitly.
        return self._create_user(username, email, password, **extra_fields)          #Calls the create user to actually create the user

    def create_superuser(self, username, email, password=None, **extra_fields):         ##A method for creating a superuser specifically.
        extra_fields.setdefault("is_staff", True)                                       ##Sets the is staff to true by default for the superuser
        extra_fields.setdefault("is_superuser", True)                                    ##Sets the is superuser to true for the superuser

        if extra_fields.get("is_staff") is not True:                                    ##Checks if isstaff and is superuser are true and raises and error if not.
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)              #Finally calls on the create user method if it passes all the checks
    


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
    