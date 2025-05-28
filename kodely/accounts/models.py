from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, uid, name=None, photo_url=None, bio=None):
        if not email:
            raise ValueError("El usuario debe tener un email")
        user = self.model(
            email=self.normalize_email(email),
            uid=uid,
            name=name,
            photo_url=photo_url,
            bio=bio,
        )
        user.set_unusable_password()  # No se usa contraseña, viene de Firebase
        user.save(using=self._db)
        return user

    def create_superuser(self, email, uid, name=None, photo_url=None, bio=None):
        user = self.create_user(email, uid, name, photo_url, bio)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None
    uid = models.CharField(max_length=128, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    photo_url = models.URLField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['uid']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


