from django.db import models

from django.contrib.auth.models import BaseUserManager ,AbstractBaseUser


class UserManager(BaseUserManager):
    use_in_migrations: True

    def create_user(self, password, email, travel_type,  **kwargs):
       
        if not email:
            raise ValueError('must have user email')
 
        user = self.model(
        
            password = password,
            email = self.normalize_email(email),
            travel_type = travel_type
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, email, travel_type, **extra_fields):

        superuser = self.create_user(
            password = password,
            email = email,
            travel_type = travel_type,

            )

        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save(using=self._db)
        return superuser
    
    
class User(AbstractBaseUser):
    
    password = models.TextField(unique=True, blank=False, null=False, max_length=15, default='')
    email = models.CharField(unique=True, blank=False, null=False, max_length=255)
    travel_type = models.CharField(unique=True, blank=False, null=False, max_length=255)
    # one to many : models.ForeignKey
    
    is_active = models.BooleanField(default=True)    
    is_admin = models.BooleanField(default=False)
    
    # 헬퍼 클래스 사용
    objects = UserManager()

    # 사용자의 username field는 nickname으로 설정
    USERNAME_FIELD = 'email'
    # 필수로 작성해야하는 field
    REQUIRED_FIELDS = ['email', 'password']

    def __str__(self):
        return self.password
    
    
    class Meta:
        db_table = 'user'


# Create your models here.
class Region(models.Model):
    name = models.CharField(max_length=20)
    region_large = models.CharField(max_length=20)
    latitude = models.IntegerField()
    longtitude = models.IntegerField()

    def __str__(self):
        return self.name
        
class PlaceType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Place(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    latitude = models.IntegerField()
    longtitude = models.IntegerField()
    place_type = models.ForeignKey(PlaceType, verbose_name="place_type", on_delete=models.CASCADE)
    region = models.ForeignKey(Region, verbose_name="region", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    
