from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.db.models.fields import related
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

class UserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class Ocupation(models.Model):
    name = models.CharField("職業",max_length=30)
    def __str__(self):
        return self.name
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('メールアドレス', unique=True, )
    name = models.CharField(('ニックネーム'), max_length=30,)
    max_listening= models.IntegerField(('ベストリスニングスコア'),  blank=True,null=True, )
    max_reading= models.IntegerField(('ベストリーディングスコア'),  blank=True,null=True,validators=[MinValueValidator(0), MaxValueValidator(495)])
    first_listening =models.IntegerField(('初めてのリスニングスコア'),blank=True,null=True,validators=[MinValueValidator(0), MaxValueValidator(495)])
    first_reading =models.IntegerField(('初めてのリーディングスコア'),blank=True,null=True,validators=[MinValueValidator(0), MaxValueValidator(495)])
    ocupation = models.ForeignKey(Ocupation,blank=True, null=True, on_delete=models.CASCADE,)
    created = models.DateTimeField(('入会日'), default=timezone.now)
    icon = models.ImageField(upload_to='images', verbose_name='プロフィール画像', default="img/user.png", null=True, blank=True) # 追加
    content = models.CharField('自己紹介',blank=True, max_length=100)

    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        ('active'),
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
    
    def __str__(self):
        return self.name

