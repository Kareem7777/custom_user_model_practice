from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
  def create_user(self,  username, email, first_name, last_name, password=None):
    if not username:
      raise ValueError('Users must have a username')
    if not email:
      raise ValueError('Users must have a email address')
    if not first_name:
      raise ValueError('Users must have a first name')
    user_obj = self.model(
      email = self.normalize_email(email),
      username = username,
      first_name = first_name,
      last_name = last_name,
    )
    user_obj.set_password(password)
    user_obj.save(using=self.db)
    return user_obj

  def create_staffuser(self, email, username, first_name, last_name, password=None):
    user = self.create_user(
      email = self.normalize_email(email),
      password = password,
      username = username,
      first_name = first_name,
      last_name = last_name,
      is_staff = True
    )
    return user

  def create_adminuser(self, email, username, first_name, last_name, password=None):
    user = self.create_user(
      email = self.normalize_email(email),
      password = password,
      username = username,
      first_name = first_name,
      last_name = last_name,
      is_staff = True,
      is_admin = True
    )
    return user

  def create_superuser(self, email, username, first_name, last_name, password=None):
    user = self.create_user(
      email = self.normalize_email(email),
      password = password,
      username = username,
      first_name = first_name,
      last_name = last_name,
    )
    user.is_staff = True
    user.is_admin = True
    user.is_superuser = True
    user.save(using=self.db)
    return user

class User(AbstractBaseUser):
  username = models.CharField(unique=True, max_length=20)
  email = models.EmailField(unique=True, max_length=50, verbose_name='email')
  date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
  is_admin = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)
  first_name = models.CharField(max_length=20)
  last_name = models.CharField(max_length=20)
  activated = models.BooleanField(default=False)
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

  objects = UserManager()

  def __str__(self):
    return self.email

  def get_full_name(self):
    if self.last_name:
      return self.first_name + self.last_name
    else:
      return self.first_name
  def get_short_name(self):
    return self.first_name

  def has_perm(self, perm, obj=None):
    return self.is_admin

  def has_module_perms(self, app_label):
    return True
