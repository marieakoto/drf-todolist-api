class ValidationError(Exception):
    pass

class UserValidator:
    @staticmethod
    def validate_username(username):
        if not username:
            raise ValidationError("Ensure the given username has been set")

    @staticmethod
    def validate_email(email):
        if not email:
            raise ValidationError("Ensure the given email has been set")

    @staticmethod
    def validate_superuser_fields(extra_fields):
        is_staff = extra_fields.get("is_staff", False)
        is_superuser = extra_fields.get("is_superuser", False)
        if not is_staff:
            raise ValidationError("Superuser must have is_staff = True")
        if not is_superuser:
            raise ValidationError("Superuser must have is_superuser = True")

    @staticmethod
    def validate_user_fields(extra_fields):
        is_staff = extra_fields.get("is_staff", False)
        is_superuser = extra_fields.get("is_superuser", False)
        if is_staff:
            raise ValidationError("User must have is_staff = False")
        if is_superuser:
            raise ValidationError("User must have is_superuser = False")
