

class NoUsernameError(ValueError):
    message = "Ensure the given username has been set"

class NoEmailError(ValueError):
    message = "Ensure the given email has been set"

class SuperuserMustHaveStaffError(ValueError):
    message = "Superuser must have is_staff = True"

class SuperuserMustHaveSuperuserError(ValueError):
    message = "Superuser must have is_superuser = True"

class UserMustNotHaveStaffError(ValueError):
    message = "User must have is_staff = False"

class UserMustNotHaveSuperuserError(ValueError):
    message = "User must have is_superuser = False"


def validate_username(username):
    if not username:
        raise NoUsernameError()

def validate_email(email):
    if not email:
        raise NoEmailError()

def validate_superuser_fields(extra_fields):                                  
    if extra_fields.get("is_staff") is not True:                                    
        raise SuperuserMustHaveStaffError()
    if extra_fields.get("is_superuser") is not True:
        raise SuperuserMustHaveSuperuserError()

    
def validate_user_fields(extra_fields):                                  
    if extra_fields.get("is_staff") is not False:                                    
        raise UserMustNotHaveStaffError()
    if extra_fields.get("is_superuser") is not False:
        raise UserMustNotHaveSuperuserError()
    
