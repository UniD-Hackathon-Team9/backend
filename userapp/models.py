from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email=None, password=None):
        if not username:
            raise ValueError('must have user username!')
        user = self.model(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        superuser = self.create_user(
            username=username,
            email=email,
            password=password
        )
        superuser.is_admin = True
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.save()
        return superuser

class User(AbstractBaseUser):
    class PersonType(models.TextChoices):
        a = 'a'
        b = 'b'
        c = 'c'
        d = 'd'
        e = 'e'

    objects = UserManager()

    username = models.CharField(max_length=20, null=False, unique=True)
    email = models.EmailField(max_length=50, null=False)
    person_type = models.CharField(max_length=2, null=True, choices=PersonType.choices)
    select_view = models.BooleanField(null=True)
    select_cafe = models.BooleanField(null=True)
    select_drink = models.BooleanField(null=True)
    select_food = models.BooleanField(null=True)
    select_activity = models.BooleanField(null=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email']

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin