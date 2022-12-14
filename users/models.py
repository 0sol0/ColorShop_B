from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from image_optimizer.fields import OptimizedImageField

class UserManager(BaseUserManager):
    def create_user(self, username, nickname, password=None):
        if not username:
            raise ValueError('유저이름을 작성해주세요.')

        user = self.model(
            username=username,
            nickname=nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, nickname, password=None):
        user = self.create_user(
            username,
            nickname=nickname,
            password=password,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(
        verbose_name='username',
        max_length=20,
        unique=True,
        error_messages={'unique': "이미 존재하는 유저이름입니다."}
    )
    profile_img = OptimizedImageField(
        upload_to="uploads/%Y/%m/%d",
        optimized_image_output_size=(300, 300),
        optimized_image_resize_method="cover",
        default="bros_blank.jpg",
        null=True, blank=True
    )
    nickname = models.CharField(max_length=30, default="", blank=True, unique=True, error_messages={'unique': "이미 존재하는 닉네임입니다."})
    bio = models.CharField(max_length=255, default='', blank=True)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nickname',]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
        